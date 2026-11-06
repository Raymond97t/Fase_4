from abc import ABC, abstractmethod
import logging 


logging.basicConfig(
    filename='Error.log',
    filemode= 'w',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s - %(lineno)d - %(filename)s',
    encoding='utf-8'
)

