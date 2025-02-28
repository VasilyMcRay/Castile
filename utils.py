def format_proxy(proxy: str, protocol: str = 'http') -> str:
    """
    Функция для форматирования прокси в http или socks5.

    Args:
        proxy (str): Прокси в любом формате (ip:port, username:password@ip:port и т.д.).
        protocol (str): Требуемый протокол ('http' или 'socks5').

    Returns:
        str: Прокси в формате protocol://username:password@ip:port.

    Raises:
        ValueError: Если формат прокси неверен или если указан неподдерживаемый протокол.
    """
    # Поддерживаемые протоколы
    supported_protocols = ['http', 'socks5']
    if protocol not in supported_protocols:
        raise ValueError(f"Unsupported protocol: {protocol}. Supported protocols are: {', '.join(supported_protocols)}")

    # Разделим прокси на компоненты
    try:
        if '@' in proxy:  # Если есть логин и пароль
            auth, endpoint = proxy.split('@')
            username, password = auth.split(':')
        else:  # Если логина и пароля нет
            username = password = None
            endpoint = proxy

        # Разделяем IP и порт
        ip, port = endpoint.split(':')
    except ValueError:
        raise ValueError(f"Invalid proxy format: {proxy}. Expected formats: ip:port, username:password@ip:port.")

    # Формируем строку
    if username and password:
        formatted_proxy = f"{protocol}://{username}:{password}@{ip}:{port}"
    else:
        formatted_proxy = f"{protocol}://{ip}:{port}"

    return formatted_proxy
