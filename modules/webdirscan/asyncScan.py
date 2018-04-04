from urllib import parse as urlparse
import aiofiles
import argparse
import asyncio
import aiohttp
import random
import sys
import os


class AsyncScan:

    USER_AGENT = [
        "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1",
        "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'",
        "Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);"
    ]

    def __init__(self, website, dict_path, timeout=3, concurrent_num=10):
        """
        初始化
        :param website: 目标站点
        :param dict_path:  字典路径
        :param timeout: 超时时间
        :param concurrent_num: 并发数
        """
        self.dictionary_path = dict_path if os.path.isabs(dict_path) else os.path.join(sys.path[0], dict_path)
        website = website if 'http://' in website or 'https://' in website else 'http://{url}'.format(url=website)
        self.target_site = website if website[-1] == '/' else website + '/'
        self.timeout = timeout
        self.queue = asyncio.Queue()
        self.concurrent_num = concurrent_num

    async def init_queue(self):
        async for path in self.get_path():
            await self.queue.put(urlparse.urljoin(self.target_site, path))

    async def get_path(self):
        async with aiofiles.open(self.dictionary_path, encoding="utf-8") as file:
            async for line in file:
                line = line.strip()
                if line == "":
                    continue
                elif line[0] != "#":
                    yield line[1:] if line[0] == '/' else line

    async def web_scan(self):
        async with aiohttp.ClientSession() as session:
            await asyncio.sleep(0.1)
            while not self.queue.empty():
                url = await self.queue.get()
                async with session.head(url,
                                        timeout=self.timeout,
                                        headers={"User-Agent": random.choice(self.USER_AGENT)}) as r:
                    if r.status == 200 or r.status == 403:
                        print("[{status}] {url}".format(status=r.status, url=url))

    async def run(self, loop):
        consumers = [loop.create_task(self.web_scan()) for _ in range(self.concurrent_num)]
        await asyncio.wait(consumers + [loop.create_task(self.init_queue())])


def __usage(arg):
    description = "webscan is a simple web scan tools"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("scanUrl", help="the website to be scan", type=str)
    parser.add_argument("-d", "--dict", dest="scanDict", help="the dictionary for scan", type=str, default="dict.txt")
    parser.add_argument("-c", "--concurrent", dest="concurrentNum", help="concurrent number", type=int, default=10)
    args = parser.parse_args(arg)
    return args


def dir_scan(args):
    args = __usage(args)
    scan = AsyncScan(args.scanUrl, args.scanDict, args.concurrentNum)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(scan.run(loop))
    except KeyboardInterrupt:
        print('\nExit ...')

        # https://stackoverflow.com/questions/30765606/whats-the-correct-way-to-clean-up-after-an-interrupted-event-loop?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
        # Do not show `asyncio.CancelledError` exceptions during shutdown
        # (a lot of these may be generated, skip this if you prefer to see them)
        def shutdown_exception_handler(loop, context):
            if "exception" not in context \
                    or not isinstance(context["exception"], asyncio.CancelledError):
                loop.default_exception_handler(context)

        loop.set_exception_handler(shutdown_exception_handler)

        # Handle shutdown gracefully by waiting for all tasks to be cancelled
        tasks = asyncio.gather(*asyncio.Task.all_tasks(loop=loop), loop=loop, return_exceptions=True)
        tasks.add_done_callback(lambda t: loop.stop())
        tasks.cancel()

        # Keep the event loop running until it is either destroyed or all
        # tasks have really terminated
        while not tasks.done() and not loop.is_closed():
            loop.run_forever()
    finally:
        loop.close()


if __name__ == '__main__':
    # import urllib.request, time
    # AsyncScan('www.baidu.com', 'dict/dict.txt')
    # AsyncScan.run()
    pass

