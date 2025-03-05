import socket
import time
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from colorama import Fore, Style, init

# 初始化彩色终端
init(autoreset=True)

def port_scan(host, port):
    """扫描指定主机的单个端口"""

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((host, port))
        banner = banner_grab(s)  # 获取端口的 Banner
        s.close()
        return port, banner
    except Exception:
        return None, None

def banner_grab(s):
    """尝试获取服务的 Banner 信息"""
    try:
        s.send(b"HEAD / HTTP/1.1\r\n\r\n")  # 发送 HTTP 请求
        return s.recv(1024).decode(errors="ignore").strip()[:50]  # 取前50个字符
    except:
        return "未知服务"

def get_service_name(port):
    """根据端口号获取标准服务名称"""
    try:
        return socket.getservbyport(port)
    except:
        return "未知服务"

def user_input(input_str):
    """解析端口输入"""

    port_list = list()
    if '-' in input_str:
        start, end = input_str.split('-')
        port_list.extend(range(int(start), int(end) + 1))
    elif ',' in input_str:
        port_list = [int(p) for p in input_str.split(',')]
    else:
        port_list.append(int(input_str))
    return port_list

def print_banner():
    """打印欢迎横幅"""

    print(f"\n{Fore.CYAN}=== 端口扫描器 v1.2 ===")
    print(f"{Fore.YELLOW}• 支持多线程扫描")
    print(f"• 支持端口范围/列表/单个端口")
    print(f"• 探测端口对应的服务{Style.RESET_ALL}\n")

def main():
    print_banner()

    # 用户输入处理
    try:
        input_str = input(f"{Fore.GREEN}[?] 请输入目标 (格式: 主机 端口范围){Fore.WHITE}\n"
                          f"{Fore.LIGHTBLACK_EX}示例: 127.0.0.1 80-100 / 192.168.1.1 22,80,443 / 172.16.1.2 80 \n"
                          f"{Fore.CYAN}» ")
        host, ports_str = input_str.strip().split(' ', 1)
        port_list = user_input(ports_str)
    except Exception:
        print(f"{Fore.RED}[!] 输入格式错误，请参考示例！")
        return

    # 扫描进度条
    print(f"\n{Fore.MAGENTA}[*] 开始扫描 {host} (共 {len(port_list)} 个端口)...")
    start_time = time.time()

    # 使用线程池并发扫描，建议线程数50-200
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(port_scan, host, port) for port in port_list]

        # 使用进度条
        with tqdm(total=len(port_list), unit="port",
                  bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.BLUE, Fore.RESET)) as pbar:
            for future in futures:
                port, banner = future.result()
                if port is not None:
                    service_name = get_service_name(port)
                    open_ports.append((port, service_name, banner))
                pbar.update(1)

    # 结果输出
    print(f"\n{Fore.GREEN}[✓] 扫描完成！耗时 {time.time() - start_time:.2f} 秒")
    if open_ports:
        print(f"{Fore.CYAN}[+] 开放端口列表:")
        open_ports.sort()
        for port, service, banner in open_ports:
            print(f"  {Fore.WHITE}→ {Fore.GREEN}{host}:{port}/tcp{Fore.YELLOW} [{service}]")
            print(f"    {Fore.LIGHTBLACK_EX}Banner: {banner}")
    else:
        print(f"{Fore.RED}[-] 未发现开放端口")

if __name__ == "__main__":
    main()
