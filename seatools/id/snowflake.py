import time
import threading


class Snowflake:
    """雪花ID生成工具

    使用方式:
        s = Snowflake(datacenter_id=1, worker_id=1) # 根据业务场景给不同机器设置不同的datacenter_id与worker_id
        unique_id = s.next_id() # 获取ID
    """

    def __init__(self, datacenter_id: int = 1, worker_id: int = 1):
        """

        Args:
            datacenter_id: 数据中心ID
            worker_id: 工单节点ID
        """
        self._datacenter_id = datacenter_id
        self._worker_id = worker_id
        self._epoch = 1288834974657
        self._timestamp_left_shift = 22
        self._sequence = 0
        self._last_timestamp = -1
        # 初始化锁
        self._lock = threading.Lock()

    def next_id(self):
        with self._lock:  # 使用锁来同步线程
            current_timestamp = self._get_timestamp()
            if current_timestamp < self._last_timestamp:
                raise Exception("Clock moved backwards. Refusing to generate id")

            if current_timestamp == self._last_timestamp:
                self._sequence = (self._sequence + 1) & 0xfff
                if self._sequence == 0:
                    current_timestamp = self._til_next_millis(self._last_timestamp)
            else:
                self._sequence = 0

            self._last_timestamp = current_timestamp

            return ((current_timestamp - self._epoch) << self._timestamp_left_shift) | \
                (self._datacenter_id << 12) | \
                (self._worker_id << 7) | \
                self._sequence

    def _get_timestamp(self):
        return int(time.time() * 1000)

    def _til_next_millis(self, _last_timestamp):
        while True:
            current_timestamp = self._get_timestamp()
            if current_timestamp > _last_timestamp:
                return current_timestamp
