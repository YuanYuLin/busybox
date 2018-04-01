import ops
import iopc

pkg_path = ""
output_dir = ""
busybox_tarball = ""
busybox_def_config = ""
busybox_build_dir = ""
busybox_install_dir = ""
src_busybox_udhcpc_script = ""
src_busybox_inittab = ""
jobs_count = ""

def set_global(args):
    global pkg_path
    global output_dir
    global busybox_tarball
    global busybox_def_config
    global busybox_build_dir
    global busybox_install_dir
    global src_busybox_udhcpc_script
    global src_busybox_inittab
    global jobs_count

    pkg_args = args["pkg_args"]
    def_cfg_version = "default_" + pkg_args["config"] + ".config"
    BUSYBOX_VERSION = pkg_args["version"]
    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    jobs_count = ops.getEnv("BUILD_JOBS_COUNT")
    busybox_tarball = ops.path_join(pkg_path, BUSYBOX_VERSION) + ".tar.bz2"
    busybox_def_config = ops.path_join(pkg_path, def_cfg_version)
    busybox_build_dir = ops.path_join(output_dir, BUSYBOX_VERSION)
    busybox_install_dir = ops.path_join(output_dir, "busybox-bin")
    #src_busybox_udhcpc_script = ops.path_join(busybox_build_dir, "examples/udhcp/simple.script")
    src_busybox_udhcpc_script = ops.path_join(pkg_path, "default.script")
    src_busybox_inittab = ops.path_join(pkg_path, "inittab")
    #dst_busybox_udhcpc_script_dir = iopc.getBinPkgPath(args["pkg_name"]) + "/usr/share/udhcpc/"
    if jobs_count == "" :
        jobs_count = "2"

def MAIN_ENV(args):
    set_global(args)

    ops.exportEnv(ops.setEnv("busybox_tarball", busybox_tarball))
    ops.exportEnv(ops.setEnv("busybox_build_dir", busybox_build_dir))
    ops.exportEnv(ops.setEnv("busybox_def_config", busybox_def_config))
    return False

def MAIN_EXTRACT(args):
    set_global(args)

    ops.unTarBz2(busybox_tarball, output_dir)
    return True

def MAIN_CONFIGURE(args):
    set_global(args)

    ops.copyto(busybox_def_config, ops.path_join(busybox_build_dir, ".config"))
    return True

def MAIN_PATCH(args, patch_group_name):
    set_global(args)
    for patch in iopc.get_patch_list(pkg_path, patch_group_name):
        if iopc.apply_patch(output_dir, patch):
            continue
        else:
            sys.exit(1)

    return True

def MAIN_BUILD(args):
    set_global(args)

    print busybox_build_dir
    extra_conf = []
    extra_conf.append("-j" + jobs_count)
    #extra_conf = []
    #extra_conf.append("ARCH=" + ops.getEnv("ARCH"))
    #extra_conf.append("CROSS_COMPILE=" + ops.getEnv("CROSS_COMPILE"))
    iopc.make(busybox_build_dir, extra_conf)
    return False

def MAIN_INSTALL(args):
    set_global(args)

    ops.mkdir(busybox_install_dir)
    extra_conf = []
    #extra_conf.append("CONFIG_PREFIX=" + iopc.getBinPkgPath(args["pkg_name"]))
    extra_conf.append("CONFIG_PREFIX=" + busybox_install_dir)
    iopc.make_install(busybox_build_dir, extra_conf)

    ops.mkdir(ops.path_join(busybox_install_dir, "usr/share/udhcpc"))
    ops.copyto(src_busybox_udhcpc_script, ops.path_join(busybox_install_dir, "usr/share/udhcpc"))

    ops.mkdir(ops.path_join(busybox_install_dir, "etc"))
    ops.copyto(src_busybox_inittab, ops.path_join(busybox_install_dir, "etc"))
    ops.ln(busybox_install_dir, "/sbin/init", "init")
    #iopc.installBin(args["pkg_name"], tmp_busybox_udhcpc_script, "/usr/share/udhcpc/")
    #iopc.installBin(args["pkg_name"], dst_busybox_inittab, "/etc")
    iopc.installBin(args["pkg_name"], ops.path_join(busybox_install_dir, "."), ".")
    #ops.ln(install_dir, "/sbin/init", "init")
    return False

def MAIN_CLEAN_BUILD(args):
    set_global(args)

    return False

def MAIN(args):
    set_global(args)

    print "busybox"

