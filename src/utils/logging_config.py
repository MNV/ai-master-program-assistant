import logging
import logging.config
import yaml


def setup_logging(config_path: str = "config.yaml") -> None:
    """
    Настраивает логирование на основании раздела 'logging' в config.yaml.

    Пример конфигурации в YAML:
    logging:
      version: 1
      formatters:
        default:
          format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
      handlers:
        console:
          class: logging.StreamHandler
          formatter: default
          level: INFO
      root:
        level: INFO
        handlers: [console]
    """
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f).get("logging", {})

    if cfg:
        logging.config.dictConfig(cfg)
    else:
        # если раздел logging не найден — базовая настройка
        logging.basicConfig(level=logging.INFO)
