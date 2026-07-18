import logging

def get_logger(name:str):
    
    try:
        
        if not name:
            raise ValueError("Logger name cannot be empty")
        
        name = name.join("-logger")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        logger = logging.getLogger(name)
        return logger
        
    except ValueError as e:
        print(f'Value error: {e}')
        raise
    
    except Exception as e:
        print(f"Error in {name}: {e}")
        raise
    