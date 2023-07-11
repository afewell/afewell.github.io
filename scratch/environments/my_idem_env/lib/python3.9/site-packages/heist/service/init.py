async def disable(hub, tunnel_plugin, target_name, service):
    await hub.service[hub.OPT.heist.service_plugin].disable(
        tunnel_plugin, target_name, service
    )


async def enable(hub, tunnel_plugin, target_name, service):
    await hub.service[hub.OPT.heist.service_plugin].enable(
        tunnel_plugin, target_name, service
    )


async def start(hub, tunnel_plugin, target_name, service, **kwargs):
    await hub.service[hub.OPT.heist.service_plugin].start(
        tunnel_plugin, target_name, service, **kwargs
    )


async def stop(hub, tunnel_plugin, target_name, service):
    await hub.service[hub.OPT.heist.service_plugin].stop(
        tunnel_plugin, target_name, service
    )


async def restart(hub, tunnel_plugin, target_name, service):
    await hub.service[hub.OPT.heist.service_plugin].restart(
        tunnel_plugin, target_name, service
    )


def get_service_plugin(hub, remote=None, grains=None):
    """
    Return the serivce manager plugin that should be used.
    """
    if not grains:
        grains = {}

    if not remote:
        remote = {}

    # Get plugin from Heist config first
    service_plugin = hub.OPT.heist.get("service_plugin")

    # Will be overwritten by auto_service, if configured
    if hub.OPT.heist.auto_service:
        if "init" in grains:
            hub.log.debug("Auto detecting the service manager")
            service_plugin = grains["init"]
        else:
            hub.log.error("Could not auto detect the service")

    # Will be overwritten by roster.cfg if defined
    if "service_plugin" in remote:
        service_plugin = remote["service_plugin"]
    return service_plugin


def service_conf_path(hub, service_name, service_plugin=None):
    if not service_plugin:
        service_plugin = hub.service.init.get_service_plugin()
    conf_path = hub.service[service_plugin].conf_path(service_name)
    if not conf_path:
        return ""
    return conf_path


async def clean(hub, target_name, tunnel_plugin, service_name, service_plugin):
    # stop service
    await hub.service[hub.heist.CONS[target_name]["service_plugin"]].stop(
        tunnel_plugin, target_name, service_name
    )

    service_conf = hub.service.init.service_conf_path(service_name)
    if service_conf:
        ret = await hub.tunnel[tunnel_plugin].cmd(target_name, f"[ -f {service_conf} ]")
        if ret.returncode == 0:
            await hub.tunnel[tunnel_plugin].cmd(target_name, f"rm -f {service_conf}")
        else:
            hub.log.error(
                f"The conf file {service_conf} does not exist. Will not attempt to remove"
            )

    await hub.service[service_plugin].clean(target_name, tunnel_plugin, service_name)
