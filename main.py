"""
Modular RAG MCP Server - Main Entry Point

Starts the MCP Server with Stdio Transport for local knowledge retrieval.
"""
import sys
import os

# Add project root to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """Main entry point: load config and start MCP server."""
    from src.core.settings import load_settings
    from src.observability.logger import get_logger

    logger = get_logger(__name__)

    try:
        settings = load_settings()
        logger.info("Settings loaded successfully")
        logger.info(f"LLM provider: {settings.llm.get('provider', 'N/A')}")
        logger.info(f"Embedding provider: {settings.embedding.get('provider', 'N/A')}")
        logger.info(f"Vector store backend: {settings.vector_store.get('backend', 'N/A')}")

        # MCP Server startup will be implemented in Phase E
        logger.info("Modular RAG MCP Server initialized. MCP Server will be available after Phase E.")

    except Exception as e:
        print(f"[FATAL] Failed to start server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
