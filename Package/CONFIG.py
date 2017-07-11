import ops
import iopc

pkg_path = ""
output_dir = ""
busybox_tarball = ""
busybox_def_config = ""
busybox_build_dir = ""
src_busybox_udhcpc_script = ""
tmp_busybox_udhcpc_script = ""

def set_global(args):
    global pkg_path
    global output_dir
    global busybox_tarball
    global busybox_def_config
    global busybox_build_dir
    global src_busybox_udhcpc_script
    global tmp_busybox_udhcpc_script

    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    busybox_tarball = pkg_path + "/busybox-1.25.1.tar.bz2"
    busybox_def_config = pkg_path + "/default.config"
    busybox_build_dir = output_dir + "/busybox-1.25.1"
    src_busybox_udhcpc_script = busybox_build_dir + "/examples/udhcp/simple.script"
    tmp_busybox_udhcpc_script = ops.path_join(output_dir, "default.script")
    #dst_busybox_udhcpc_script_dir = iopc.getBinPkgPath(args["pkg_name"]) + "/usr/share/udhcpc/"

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
    iopc.make(busybox_build_dir)
    return False

def MAIN_INSTALL(args):
    set_global(args)

    extra_conf = []
    extra_conf.append("CONFIG_PREFIX=" + iopc.getBinPkgPath(args["pkg_name"]))
    iopc.make_install(busybox_build_dir, extra_conf)

    ops.copyto(src_busybox_udhcpc_script, tmp_busybox_udhcpc_script)
    iopc.installBin(args["pkg_name"], tmp_busybox_udhcpc_script, "/usr/share/udhcpc/")
    return False

def MAIN_CLEAN_BUILD(args):
    set_global(args)

    return False

def MAIN(args):
    set_global(args)

    print "busybox"

