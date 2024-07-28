from canStruct import CombustionStruct
from can.mcpDriver import McpCanBus

def txDials(mcp, struct):
    mcp.txMessage(id, length, payload, extended)