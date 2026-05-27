import logging
from typing import TYPE_CHECKING, Dict, Set

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .items import lookup_name_to_id
from .locations import location_data, lookup_location_to_id

from NetUtils import ClientStatus

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

ROM_ADDRS = {
    "game_identifier": (0x0134, 0x06, "ROM"),
    "slot_name": (0x3FFFF0, 0xF, "ROM")
}

RAM_ADDRS = {
    "game_state": (0xC5DB, 2, "System Bus"),
    "received_item_index": (0xCC1E, 2, "System Bus"),
    "received_item": (0xCC1D, 1, "System Bus"),
    "location_flags": (0xCBD7, 0x68, "System Bus")
}

logger = logging.getLogger()


class DQM2Client(BizHawkClient):
    game = "Dragon Quest Monsters 2"
    system = ("GBC", "SGB")
    patch_suffix = (".apdqm2t", "apdqm2c")

    local_checked_locations: Set[int]
    item_id_to_name: Dict[str, int]
    location_name_to_id: Dict[str, int]

    def __init__(self) -> None:
        super().__init__()
        self.item_id_to_name = lookup_name_to_id
        self.location_name_to_id = lookup_location_to_id
        self.local_checked_locations = set()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [ROM_ADDRS["game_identifier"]]))[0]
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            if rom_name not in ("DWM2-T", "DWM2-C"):
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b011
        ctx.watcher_timeout = 0.5

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        slot_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [ROM_ADDRS["slot_name"]]))[0]
        auth_name = slot_name_bytes.decode("ascii").split("\x00")[0]
        ctx.auth = auth_name


    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
            return

        try:
            read_result = await bizhawk.read(ctx.bizhawk_ctx, [
                RAM_ADDRS["game_state"],
                RAM_ADDRS["received_item_index"],
                RAM_ADDRS["received_item"],
                RAM_ADDRS["location_flags"]
            ])
            
            if read_result is None:
                return

            num_received_items = int.from_bytes(read_result[1], "little")
            received_item_is_empty = (read_result[2][0] == 0)
            flag_bytes = read_result[3]
            
            # Only checks for Darck, update once more goals are available
            if (flag_bytes[0xCBF1 - RAM_ADDRS["location_flags"][0]] & 0x01 == 0x01) and not ctx.finished_game:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True

            await self.process_checked_locations(ctx, flag_bytes)
            
            if received_item_is_empty:
              await self.process_received_items(ctx, num_received_items)
            

        except bizhawk.RequestFailedError:
            pass

    async def process_checked_locations(self, ctx: "BizHawkClientContext", flag_bytes):
        checked_locations = set()

        for loc_name, loc_data in location_data.items():

            byte_addr = loc_data.ram_addr.byte
            byte_offset = byte_addr - RAM_ADDRS["location_flags"][0]
            bit_mask = loc_data.ram_addr.bit_mask
            if flag_bytes[byte_offset] & bit_mask == bit_mask:
                location_id = self.location_name_to_id[loc_name]
                checked_locations.add(location_id)

        logger.info(f"{checked_locations}")
        await ctx.check_locations(checked_locations)
    
    @staticmethod
    async def process_received_items(ctx: "BizHawkClientContext", num_received_items: int):
      if num_received_items < len(ctx.items_received):
        next_item = ctx.items_received[num_received_items].item
        await bizhawk.write(ctx.bizhawk_ctx, [(0xCC1D, [next_item], "System Bus")])