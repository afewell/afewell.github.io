async def disable(hub, tunnel_plugin, target_name, service):
    ret = await hub.tunnel[tunnel_plugin].cmd(
        target_name,
        f"Set-Service -Name {service} -StartupType Disabled; "
        f"If ($?) {{ exit 0 }} else {{ exit 1 }}",
    )
    if ret.exit_status != 0:
        hub.log.error(ret.stderr)
        return False
    return True


async def enable(hub, tunnel_plugin, target_name, service):
    ret = await hub.tunnel[tunnel_plugin].cmd(
        target_name,
        f"Set-Service -Name {service} -StartupType Automatic; "
        f"If ($?) {{ exit 0 }} else {{ exit 1 }}",
    )
    if ret.exit_status != 0:
        hub.log.error(ret.stderr)
        return False
    return True


async def start(hub, tunnel_plugin, target_name, service, **kwargs):
    ret = await hub.tunnel[tunnel_plugin].cmd(
        target_name,
        f"Start-Service -Name {service}; If ($?) {{ exit 0 }} else {{ exit 1 }}",
    )
    if ret.exit_status != 0:
        hub.log.error(ret.stderr)
        return False
    return True


async def stop(hub, tunnel_plugin, target_name, service):
    ret = await hub.tunnel[tunnel_plugin].cmd(
        target_name,
        f"Stop-Service -Name {service}; If ($?) {{ exit 0 }} else {{ exit 1 }}",
    )
    if ret.exit_status != 0:
        hub.log.error(ret.stderr)
        return False
    return True


async def restart(hub, tunnel_plugin, target_name, service):
    ret = await hub.tunnel[tunnel_plugin].cmd(
        target_name,
        f"Restart-Service -Name {service}; If ($?) {{ exit 0 }} else {{ exit 1 }}",
    )
    if ret.exit_status != 0:
        hub.log.error(ret.stderr)
        return False
    return True


def conf_path(hub, service_name):
    pass


async def clean(hub, target_name, tunnel_plugin, service):
    ret = await hub.tunnel[tunnel_plugin].cmd(
        target_name, f"cmd /c sc delete {service}"
    )
    if ret.exit_status != 0:
        hub.log.error(ret.stderr)
        return False
    return True
