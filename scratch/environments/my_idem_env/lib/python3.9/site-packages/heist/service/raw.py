async def disable(hub, tunnel_plugin, target_name, service):
    pass


async def enable(hub, tunnel_plugin, target_name, service):
    pass


async def start(
    hub, tunnel_plugin, target_name, service, run_cmd=None, target_os="linux", **kwargs
):
    """
    Start the service in the background
    """
    cmd = [f"{run_cmd}"]
    ret = await hub.tunnel[tunnel_plugin].cmd(
        target_name, " ".join(cmd), background=True, target_os=target_os
    )
    if ret.returncode != 0:
        hub.log.error(ret.stderr)
        return False
    return True


async def stop(hub, tunnel_plugin, target_name, service):
    """
    Stop the service
    """
    # TODO: Need to figure out how to get target_os here
    target_os, _ = await hub.tool.system.os_arch(target_name, tunnel_plugin)
    if target_os == "windows":
        kill_cmd = (
            "Stop-Process -Name salt -ErrorAction SilentlyContinue; "
            "If ($?) { exit 0 } else { exit 1 }"
        )
    else:
        kill_cmd = f"pkill -f {service}"
    hub.log.debug(f"Attempting to kill {service} with: {kill_cmd}")
    ret = await hub.tunnel[tunnel_plugin].cmd(
        target_name, kill_cmd, target_os=target_os
    )
    if ret.exit_status != 0:
        hub.log.error(ret.stderr)
        return False
    hub.log.info(f"Successfully killed {service}")
    return True


async def restart(hub, tunnel_plugin, target_name, service):
    pass


def conf_path(hub, service_name):
    pass


async def clean(hub, target_name, tunnel_plugin, service):
    pass
