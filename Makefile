all: headers disass out

headers:
	riscv64-unknown-elf-objdump -x $(DIR)/target/release/build/methods-$(BUILD)/out/riscv-guest/riscv32im-risc0-zkvm-elf/release/$(METHOD) > logs/headers.log		

disass:
	riscv64-unknown-elf-objdump -d $(DIR)/target/release/build/methods-$(BUILD)/out/riscv-guest/riscv32im-risc0-zkvm-elf/release/$(METHOD) > logs/disass.log

out:
	-RISC0_LOG=2 $(DIR)/target/release/starter > logs/out.log 2>&1
