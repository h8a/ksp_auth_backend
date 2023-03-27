import uvicorn
from config import cfg


if __name__ == '__main__':
    uvicorn.run(
        'app:Service',
        reload=cfg.service.debug,
        factory=cfg.service.debug,
        host=cfg.service.host,
        port=cfg.service.port,
        log_level=cfg.service.log_level,
        lifespan='on'
    )