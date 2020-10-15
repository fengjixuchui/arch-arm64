#!/usr/bin/env python

RET = b'\xc0\x03\x5f\xd6'

test_cases = [
	(b'\x01\x00\x00\xd4'+RET, 'LLIL_SET_REG(syscall_imm,LLIL_CONST(0)); LLIL_SYSCALL()'), # svc #0; ret; ZwAccessCheck() on win-arm64
	(b'\x21\x00\x00\xd4'+RET, 'LLIL_SET_REG(syscall_imm,LLIL_CONST(1)); LLIL_SYSCALL()'), # svc #1; ret; ZwWorkerFactoryWorkerReady() on win-arm64
	(b'\x41\x00\x00\xd4'+RET, 'LLIL_SET_REG(syscall_imm,LLIL_CONST(2)); LLIL_SYSCALL()'), # svc #2; ret; ZwAcceptConnectPort() on win-arm64
	(b'\x61\x00\x00\xd4'+RET, 'LLIL_SET_REG(syscall_imm,LLIL_CONST(3)); LLIL_SYSCALL()'), # svc #3; ret; ZwMapUserPhysicalPagesScatter() on win-arm64
	(b'\xbf\x3f\x03\xd5', 'LLIL_INTRINSIC([],__dmb,LLIL_CALL_PARAM([]))'), # dmb sy (data memory barrier, system)
	(b'\xbf\x3e\x03\xd5', 'LLIL_INTRINSIC([],__dmb,LLIL_CALL_PARAM([]))'), # dmb st (data memory barrier, stores)
	(b'\xbf\x3a\x03\xd5', 'LLIL_INTRINSIC([],__dmb,LLIL_CALL_PARAM([]))'), # dmb ishst (data memory barrier, inner shareable domain)
	(b'\x9f\x3f\x03\xd5', 'LLIL_INTRINSIC([],__dsb,LLIL_CALL_PARAM([]))'), # dsb sy (data synchronization barrier, system)
	(b'\x9f\x3e\x03\xd5', 'LLIL_INTRINSIC([],__dsb,LLIL_CALL_PARAM([]))'), # dsb st (data synchronization barrier, stores)
	(b'\x9f\x3a\x03\xd5', 'LLIL_INTRINSIC([],__dsb,LLIL_CALL_PARAM([]))'), # dsb ishst (data synchronization barrier, inner shareable domain)
	(b'\xdf\x3f\x03\xd5', 'LLIL_INTRINSIC([],__isb,LLIL_CALL_PARAM([]))'), # isb (instruction synchronization barrier, implied system)
	(b'\x1f\x20\x03\xd5', 'LLIL_INTRINSIC([],SystemHintOp_NOP,LLIL_CALL_PARAM([]))'), # hint 0x0
	(b'\x3f\x20\x03\xd5', 'LLIL_INTRINSIC([],SystemHintOp_YIELD,LLIL_CALL_PARAM([]))'), # hint 0x1
	(b'\x5f\x20\x03\xd5', 'LLIL_INTRINSIC([],SystemHintOp_WFE,LLIL_CALL_PARAM([]))'), # hint 0x2
	(b'\x7f\x20\x03\xd5', 'LLIL_INTRINSIC([],SystemHintOp_WFI,LLIL_CALL_PARAM([]))'), # hint 0x3
	(b'\x9f\x20\x03\xd5', 'LLIL_INTRINSIC([],SystemHintOp_SEV,LLIL_CALL_PARAM([]))'), # "hint 0x4" or "sev"
	(b'\xbf\x20\x03\xd5', 'LLIL_INTRINSIC([],SystemHintOp_SEVL,LLIL_CALL_PARAM([]))'), # hint 0x5
	(b'\xdf\x20\x03\xd5', 'LLIL_INTRINSIC([],SystemHintOp_DGH,LLIL_CALL_PARAM([]))'), # hint 0x6
	(b'\x1f\x22\x03\xd5', 'LLIL_INTRINSIC([],SystemHintOp_ESB,LLIL_CALL_PARAM([]))'), # hint 0x10
	(b'\x3f\x22\x03\xd5', 'LLIL_INTRINSIC([],SystemHintOp_PSB,LLIL_CALL_PARAM([]))'), # hint 0x11
	(b'\x5f\x22\x03\xd5', 'LLIL_INTRINSIC([],SystemHintOp_TSB,LLIL_CALL_PARAM([]))'), # hint 0x12
	(b'\x9f\x22\x03\xd5', 'LLIL_INTRINSIC([],SystemHintOp_CSDB,LLIL_CALL_PARAM([]))'), # hint 0x14
	(b'\x5f\x24\x03\xd5', 'LLIL_INTRINSIC([],SystemHintOp_BTI,LLIL_CALL_PARAM([]))'), # hint 0x22
	(b'\x00\xc0\x1e\xd5', 'LLIL_INTRINSIC([vbar_el3],_WriteStatusReg,LLIL_CALL_PARAM([<il: x0>]))'), # msr vbar_el3, x0
	(b'\x00\x10\x1e\xd5', 'LLIL_INTRINSIC([sctlr_el3],_WriteStatusReg,LLIL_CALL_PARAM([<il: x0>]))'), # msr sctlr_el3, x0
	(b'\xff\x44\x03\xd5', 'LLIL_INTRINSIC([daifclr],_WriteStatusReg,LLIL_CALL_PARAM([<il: 4>]))'), # msr daifclr, #0x4
	(b'\x00\x10\x3e\xd5', 'LLIL_INTRINSIC([x0],_ReadStatusReg,LLIL_CALL_PARAM([<il: sctlr_el3>]))'), # mrs x0, sctlr_el3
	(b'\x7f\x20\x03\xd5', 'LLIL_INTRINSIC([],__wfi,LLIL_CALL_PARAM([]))'), # wfi (wait for interrupt)
	(b'\x5f\x20\x03\xd5', 'LLIL_INTRINSIC([],__wfe,LLIL_CALL_PARAM([]))'), # wfe (wait for event)

#	(b'\xC1\x48\x52\x7A', 'LLIL_IF(LLIL_FLAG(n),1,3); LLIL_SUB(LLIL_REG(w6),LLIL_CONST(18)); LLIL_GOTO(8); LLIL_SET_FLAG(n,LLIL_CONST(0)); LLIL_SET_FLAG(z,LLIL_CONST(0)); LLIL_SET_FLAG(c,LLIL_CONST(0)); LLIL_SET_FLAG(v,LLIL_CONST(1)); LLIL_GOTO(8)'), # ccmp w6, #18, #1, mi
#
#	# this is funky: LLIL_SUB() is optmized away, and we needed it for the IL_FLAGWRITE_ALL, did it have effect?
#	(b'\x62\x08\x40\x7A', 'LLIL_IF(LLIL_FLAG(z),1,3); LLIL_REG(w3); LLIL_GOTO(8); LLIL_SET_FLAG(n,LLIL_CONST(0)); LLIL_SET_FLAG(z,LLIL_CONST(0)); LLIL_SET_FLAG(c,LLIL_CONST(1)); LLIL_SET_FLAG(v,LLIL_CONST(0)); LLIL_GOTO(8)'), # ccmp w3, #0, #2, eq
#	(b'\x43\xBA\x59\x7A', 'foo'), # ccmp w18, #25, #3, lt
#	(b'\xC4\x29\x5B\x7A', 'foo'), # ccmp w14, #27, #4, hs
#	(b'\x24\x08\x5B\x7A', 'foo'), # ccmp w1, #27, #4, eq
#	(b'\x22\x6A\x41\x7A', 'foo'), # ccmp w17, #1, #2, vs
#	(b'\xA8\xA8\x41\x7A', 'foo'), # ccmp w5, #1, #8, ge
#	(b'\x08\x49\x5E\x7A', 'foo'), # ccmp w8, #30, #8, mi
	(b'\x0a\x00\x80\x52', 'LLIL_SET_REG(w10,LLIL_CONST(0))'), # mov 10, #0
	(b'\x1f\x20\x03\xd5', ''), # nop, gets optimized from function
]

import sys
import binaryninja
from binaryninja import core
from binaryninja import binaryview
from binaryninja import lowlevelil

def il2str(il):
	if isinstance(il, lowlevelil.LowLevelILInstruction):
		return '%s(%s)' % (il.operation.name, ','.join([il2str(o) for o in il.operands]))
	else:
		return str(il)

# TODO: make this less hacky
def instr_to_il(data):
	RETURN = b'\xc0\x03\x5f\xd6'

	platform = binaryninja.Platform['linux-aarch64']
	# make a pretend function that returns
	bv = binaryview.BinaryView.new(data + RETURN)
	bv.add_function(0, plat=platform)
	assert len(bv.functions) == 1

	result = []
	for block in bv.functions[0].low_level_il:
		for il in block:
			result.append(il2str(il))
	result = '; '.join(result)
	assert result.endswith('LLIL_RET(LLIL_REG(x30))'), \
			'%s didnt lift to function ending in ret, got: %s' % (data.hex(), result)
	result = result[0:result.index('LLIL_RET(LLIL_REG(x30))')]
	if result.endswith('; '):
		result = result[0:-2]

	return result

if __name__ == '__main__':
	for (test_i, (data, expected)) in enumerate(test_cases):
		actual = instr_to_il(data)
		if actual != expected:
			print('MISMATCH AT TEST %d!' % test_i)
			print('\t   input: %s' % data.hex())
			print('\texpected: %s' % expected)
			print('\t  actual: %s' % actual)
			sys.exit(-1)

	print('success!')
	sys.exit(0)
