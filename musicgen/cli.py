import sys
import threading
import time
from musicgen.srv import MusicManager
from musicgen.config import Config
import os
from argparse import ArgumentParser
import signal

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_PATH = os.path.join(CURRENT_DIR,'config/config.yml')


def _get_args():
    parser = ArgumentParser()
    parser.add_argument( "-c", "--config-path", type=str, default=DEFAULT_CONFIG_PATH,
                        help="config yaml file path, default to %(default)r")
    parser.add_argument( "-d", "--description", type=str, default=None,
                        help="描述")
    parser.add_argument( "-f", "--output-file", type=str, default=None,
                        help="文件名")
    parser.add_argument( "-n","--num-musics", type=int, default=1,
                        help="音频数量")
    args = parser.parse_args()
    return args


SHUT_DOWN_EVENT = threading.Event()
SHUTDOWN_SIGNAL_RECEIVED = False # 设置一个标志，初始时为 False

def signal_handler(sig, frame):
    print("SHUT DOWN!")
    global SHUTDOWN_SIGNAL_RECEIVED
    # 检查标志是否已经被设置
    if SHUTDOWN_SIGNAL_RECEIVED:
        # 如果已经接收到信号，直接返回
        return
    # 设置标志，表示信号已经接收
    SHUTDOWN_SIGNAL_RECEIVED = True
    SHUT_DOWN_EVENT.set()
    print("good bye!")
    sys.exit(0)


def main():
    threads = []

    args = _get_args() # set launch arguments
    Config(DEFAULT_CONFIG_PATH) # load config yaml
    signal.signal(signal.SIGINT, signal_handler)  # 注册Ctrl+C信号处理程序

    # 初始化 pv_music 对象
    manager = MusicManager(Config().cli["task"],Config().cli["model"])
    music_t = threading.Thread(target=manager.generate_music, args=(args.description, args.output_file, SHUT_DOWN_EVENT, args.num_musics))
    music_t.start()
    threads.append(music_t)
    
    while True:
        try:
            time.sleep(1000)  # 模拟程序持续运行中
        except KeyboardInterrupt:
            # 如果发生 KeyboardInterrupt，例如在 time.sleep() 中按下了 Ctrl+C
            print('\n发生 KeyboardInterrupt，程序继续运行...')
            break
    for t in threads:
        t.join()

    print("Done!")


if __name__ == "__main__":
    main()