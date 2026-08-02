from langgraph.checkpoint.memory import MemorySaver

class GraphCheckpointer:
    """
    Abstracts persistence away from LangGraph primitives.
    Currently hardcoded to MemorySaver as per Phase 11.6 constraints.
    Future phases will swap this for AsyncPostgresSaver dynamically.
    """
    
    _instance = None
    
    @classmethod
    def get_saver(cls):
        if cls._instance is None:
            cls._instance = MemorySaver()
        return cls._instance
