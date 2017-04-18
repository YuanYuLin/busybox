import ops

def MAIN(args):
    output_path=ops.pkg_mkdir(args["pkg_path"], "debian_jessie_armhf")
    qemu_path=ops.pkg_mkdir(output_path, "/usr/bin")
    print qemu_path
    ops.copyto("/usr/bin/qemu-arm-static", output_path + "/usr/bin/qemu-arm-static")
    arch="armhf"
    CMD=["debootstrap", "--arch=" + arch, "--variant=minbase", "jessie", output_path]
    res = ops.execCmd(CMD, output_path, False, None)
