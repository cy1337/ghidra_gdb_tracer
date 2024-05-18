from ghidra.program.model.listing import Function
import os
from javax.swing import JFileChooser
from java.io import File

def choose_file_to_save():
    file_chooser = JFileChooser()
    file_chooser.setDialogType(JFileChooser.SAVE_DIALOG)
    user_action = file_chooser.showSaveDialog(None)
    
    if user_action == JFileChooser.APPROVE_OPTION:
        selected_file = file_chooser.getSelectedFile()
        return selected_file.getAbsolutePath()
    else:
        return None

output_path = choose_file_to_save()
if output_path:
    print("File to be saved: {}".format(output_path))
else:
    print("No output path specified")

def generate_gdb_script(output_path, symbol_name="read"):
    sym_table = currentProgram.getSymbolTable()
    static_addr = None
    for symbol in sym_table.getPrimarySymbolIterator(True):
        if symbol.getName() == symbol_name:
            static_addr = symbol.getAddress()
            break

    if static_addr is None:
        raise RuntimeError("Expected symbol {} not found".format(static_addr))

    static_addr_offset = static_addr.getOffset()
    with open(output_path, 'w') as gdb_script:
        gdb_script.write("import gdb\n\n")
        gdb_script.write("gdb.execute('set logging off')\n")
        gdb_script.write("gdb.execute('set logging file ./gdb_trace_log.txt')\n")
        gdb_script.write("gdb.execute('set logging on')\n")
        gdb_script.write("gdb.execute('set pagination off')\n")
        gdb_script.write("class FunctionBreakpoint(gdb.Breakpoint):\n")
        gdb_script.write("    def __init__(self, location, func_name):\n")
        gdb_script.write("        location += base_addr\n")
        gdb_script.write("        bp_loc = '*{}'.format(hex(location))\n")
        gdb_script.write("        super(FunctionBreakpoint, self).__init__(bp_loc, gdb.BP_BREAKPOINT, internal=False)\n")
        gdb_script.write("        self.func_name = func_name\n\n")
        gdb_script.write("    def stop(self):\n")
        gdb_script.write("        gdb.write('Function: {}\\n'.format(self.func_name))\n")
        gdb_script.write("        gdb.execute('disable breakpoints {}'.format(self.number))\n")
        gdb_script.write("        return False\n\n")
        gdb_script.write("def set_base_address():\n")
        gdb_script.write("    gdb.execute('starti')\n")
        gdb_script.write("    gdb.execute('set $base_addr = {} - 0x{:x}')\n".format(symbol_name, static_addr_offset))
        gdb_script.write("    base_addr = int(gdb.parse_and_eval('$base_addr'))\n")
        gdb_script.write("    gdb.write('Base address set to: {:#x}\\n'.format(base_addr))\n")
        gdb_script.write("    return base_addr\n\n")

        gdb_script.write("base_addr = set_base_address()\n\n")
        
        # Iterate over all functions in the program
        fm = currentProgram.getFunctionManager()
        functions = fm.getFunctions(True)
        memory = currentProgram.getMemory()
        blocks = memory.getBlocks()

        artificial_blocks = []

        for block in blocks:
            # Check if the block has a specific name or comment
            if block.getComment() and "artificial" in block.getComment().lower():
                artificial_blocks.append(block)
            elif block.getName() and "artificial" in block.getName().lower():
                artificial_blocks.append(block)

        for func in functions:
            func_name = func.getName()
            func_entry = func.getEntryPoint().getOffset()
            if any(block.contains(func.getEntryPoint()) for block in artificial_blocks):
                print("Skipping function in artificial block: {}@0x{:x}".format(func_name, func_entry)) 
                continue
            gdb_script.write("FunctionBreakpoint(0x{:x}, '{}')\n".format(func_entry, func_name))

        # Resume execution of target program
        gdb_script.write("gdb.execute('continue')\n")

generate_gdb_script(output_path)
print("GDB Python script generated at {}".format(output_path))
