# A profiling tool for the RISC0 zero-knowledge virtual machine

## Quickstart
1. Set environment variable `RISC0_LOG=2` and run the desired program via RISC0
2. Report the logs in a file called `out.log` and save it in this directory.
3. Save all section headers of the ELF file in a file called `headers.log`. You can get the headers of the ELF file by running `riscv64-unknown-elf-objdump -x <ELF>`. This command can be installed by `apt-get install binutils-riscv64-linux-gnu`. Save this file in this directory.

There are already examples of `out.log` and `headers.log` files in this directory. These files are for the `risc0-rust-starter` program. There is also a `disass.log` file which contained disassembled RISC-V code. It isn't used by the profiling tool but is good for overall debugging of RISC0 code. You can obtain this by running `riscv64-unknown-elf-objdump -d <ELF>`

Currently, this tool provides an array containing the call stack at each instruction of the program and the number of instances of each instruction called during the program. 

## macOS
1. `brew install binutils`
2. `METHODS=methods-f7c7b90a01a011bf` (find the right hash for methods by `find . -name methods`)
3. `gobjdump -x target/release/build/${METHODS}/out/riscv-guest/riscv32im-risc0-zkvm-elf/release/recursive > logs/headers.log`
4. `gobjdump -d target/release/build/${METHODS}/out/riscv-guest/riscv32im-risc0-zkvm-elf/release/recursive > logs/disass.log`
5. `cargo run --release &> logs/out.log`
6. `pipenv run python3 prof.py`