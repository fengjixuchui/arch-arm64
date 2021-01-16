/*
	lldb ./cmdline -- single d503201f
	b decode
	r
*/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

#include "operations.h"
#include "encodings.h"
#include "arm64dis.h"

int verbose = 1;

char *oper_class_to_str(enum OperandClass c)
{
	switch(c) {
		case NONE: return "NONE";
		case IMM32: return "IMM32";
		case IMM64: return "IMM64";
		case FIMM32: return "FIMM32";
		case STR_IMM: return "STR_IMM";
		case REG: return "REG";
		case MULTI_REG: return "MULTIREG";
		case SYS_REG: return "SYS_REG";
		case MEM_REG: return "MEM_REG";
		case MEM_PRE_IDX: return "MEM_PRE_IDX";
		case MEM_POST_IDX: return "MEM_POST_IDX";
		case MEM_OFFSET: return "MEM_OFFSET";
		case MEM_EXTENDED: return "MEM_EXTENDED";
		case LABEL: return "LABEL";
		case CONDITION: return "CONDITION";
		case NAME: return "NAME";
		case IMPLEMENTATION_SPECIFIC: return "IMPLEMENTATION_SPECIFIC";
		default: return "ERROR";
	}
}

char *cond_to_str(enum Condition c)
{
	switch(c) {
		case COND_EQ: return "eq";
		case COND_NE: return "ne";
		case COND_CS: return "cs";
		case COND_CC: return "cc";
		case COND_MI: return "mi";
		case COND_PL: return "pl";
		case COND_VS: return "vs";
		case COND_VC: return "vc";
		case COND_HI: return "hi";
		case COND_LS: return "ls";
		case COND_GE: return "ge";
		case COND_LT: return "lt";
		case COND_GT: return "gt";
		case COND_LE: return "le";
		case COND_AL: return "al";
		case COND_NV: return "nv";
		default:
			return "ERROR";
	}
}

int disassemble(uint64_t address, uint32_t insword, char *result)
{
	int rc;
	Instruction instr;
	memset(&instr, 0, sizeof(instr));

	rc = aarch64_decompose(insword, &instr, address);
	if(verbose)
		printf("aarch64_decompose() returned %d\n", rc);
	if(rc) return rc;

	if(verbose) {
		printf("  instr.insword: %08X\n", instr.insword);
		printf(" instr.encoding: %d %s\n", instr.encoding, enc_to_str(instr.encoding));
		printf("instr.operation: %d %s\n", instr.operation, operation_to_str(instr.operation));
		for(int i=0; i<MAX_OPERANDS && instr.operands[i].operandClass!=NONE; i++) {
			printf("instr.operands[%d]\n", i);

			InstructionOperand operand = instr.operands[i];

			printf("\t.class: %s\n", oper_class_to_str(operand.operandClass));
			switch(operand.operandClass) {
				case CONDITION:
					printf("\t\t%d %s\n", operand.cond, cond_to_str(operand.cond));
					break;
				default:
					break;
			}
		}
	}

	rc = aarch64_disassemble(&instr, result, 1024);
	if(verbose)
		printf("aarch64_disassemble() returned %d\n", rc);
	if(rc) return rc;

	return 0;
}

/* main */
int main(int ac, char **av)
{
	char instxt[1024]={'\0'};

	if(ac <= 1) {
		printf("example usage:\n");
		printf("\t%s d503201f\n", av[0]);
		return -1;
	}

	if(!strcmp(av[1], "speed")) {
		srand(0xCAFE);
		for(int i=0; i<10000000; i++) {
			uint32_t insword = (rand() << 16) ^ rand();
			disassemble(0, insword, instxt);
			//printf("%08X: %s\n", 0, instxt);
		}
		return 0;
	}

	if(!strcmp(av[1], "strain") ||
	  !strcmp(av[1], "strainer") ||
	  !strcmp(av[1], "stress") ||
	  !strcmp(av[1], "stresser"))
	{
		verbose = 0;
		for(uint32_t insword=0; insword!=0xFFFFFFFF; insword++) {
			disassemble(0, insword, instxt);

			if((insword & 0xFFFFFF) == 0)
				printf("%08X: %s\n", insword, instxt);
		}
	}

	if(!strcmp(av[1], "test")) {
		srand(0xCAFE);
		while(1) {
			Instruction instr;
			memset(&instr, 0, sizeof(instr));
			uint32_t insword = (rand() << 16) ^ rand();
			aarch64_decompose(insword, &instr, 0);
			printf("%08X: %d\n", insword, instr.encoding);
		}
	}

	else {
		uint32_t insword = strtoul(av[1], NULL, 16);
		if(disassemble(0, insword, instxt) == 0)
			printf("%08X: %s\n", insword, instxt);
	}
}
