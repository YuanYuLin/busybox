import ops
import iopc

def MAIN_ENV(args):
    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    busybox_tarball = pkg_path + "/busybox-1.25.1.tar.bz2"
    busybox_def_config = pkg_path + "/default.config"
    busybox_build_dir = output_dir + "/busybox-1.25.1"

    ops.exportEnv(ops.setEnv("busybox_tarball", busybox_tarball))
    ops.exportEnv(ops.setEnv("busybox_build_dir", busybox_build_dir))
    ops.exportEnv(ops.setEnv("busybox_def_config", busybox_def_config))
    return False

def MAIN_EXTRACT(args):
    output_dir = args["output_path"]
    busybox_tarball = ops.getEnv("busybox_tarball")
    ops.unTarBz2(busybox_tarball, output_dir)
    return True

def MAIN_CONFIGURE(args):
    busybox_def_config = ops.getEnv("busybox_def_config")
    busybox_build_dir = ops.getEnv("busybox_build_dir")
    ops.copyto(busybox_def_config, busybox_build_dir + "/.config")
    return True

def MAIN_BUILD(args):
    busybox_build_dir = ops.getEnv("busybox_build_dir")
    iopc.make(busybox_build_dir)
    return False

def MAIN_INSTALL(args):
    output_dir = args["output_path"]
    busybox_build_dir = ops.getEnv("busybox_build_dir")
    extra_conf = []
    extra_conf.append("CONFIG_PREFIX=" + iopc.getBinPkgPath(args["pkg_name"]))
    iopc.make_install(busybox_build_dir, extra_conf)
    return False

def MAIN_CLEAN_BUILD(args):
    output_dir = args["output_path"]
    return False

def MAIN(args):
    print "busybox"
'''
    output_path=ops.pkg_mkdir(args["pkg_path"], "debian_jessie_armhf")
    qemu_path=ops.pkg_mkdir(output_path, "/usr/bin")
    print qemu_path
    ops.copyto("/usr/bin/qemu-arm-static", output_path + "/usr/bin/qemu-arm-static")
    arch="armhf"
    CMD=["debootstrap", "--arch=" + arch, "--variant=minbase", "jessie", output_path]
    res = ops.execCmd(CMD, output_path, False, None)
'''
