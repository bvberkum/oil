import re

import osh
from asdl import py_meta


class AstVisitor:

    """
    Todo: base for AST visitor types to build more generalized visitors.
    See-also visitor.py?
    """

    prefix = 'emit_'

    def __init__(self, sparse=False, prefix=None):
        self.sparse = sparse
        if prefix:
            self.prefix = prefix

    def visit(self, node):
        emitter = self.prefix+node.__class__.__name__
        if hasattr(self, emitter): getattr(self, emitter)(node)

        visitor = 'visit_'+node.__class__.__name__
        if self.sparse:
            if hasattr(self, visitor): getattr(self, visitor)(node)
            else: self.visit_(node)
        else:
            getattr(self, visitor)(node)

    def visit_(self, node):
        if not node or not hasattr(node, '__slots__'): return
        for key in node.__slots__:
            if not hasattr(node, key): continue
            v = getattr(node, key)
            if isinstance(v, list):
                if v and isinstance(v[0], py_meta.CompoundObj):
                    for subnode in v:
                        self.visit(subnode)
            else:
                if v and isinstance(v, py_meta.CompoundObj):
                    self.visit(v)

    def visitattr(self, node, attr):
        for subnode in getattr(node, attr):
            self.visit(subnode)

    # XXX: probably have not hooked up all nodes yet, but using the 'sparse'
    # mode doesn't need to; visit_ does any attribute pointing to an AST node

    #def visit_line_span(self, node): pass
    def visit_token(self, node): pass
    #def visit_braced_step(self, node): pass
    #def visit_bracket_op_e(self, node): pass
    #def visit_bracket_op(self, node): pass
    #def visit_WholeArray(self, node): pass
    def visit_ArrayIndex(self, node): self.visit(node.expr)
    #def visit_suffix_op_e(self, node): pass
    #def visit_suffix_op(self, node): pass
    #def visit_StringNullary(self, node): pass
    #def visit_StringUnary(self, node): pass
    #def visit_PatSub(self, node): pass
    #def visit_Slice(self, node): pass
    #def visit_array_item_e(self, node): pass
    #def visit_array_item(self, node): pass
    #def visit_ArrayWord(self, node): pass
    #def visit_ArrayPair(self, node): pass
    #def visit_word_part_e(self, node): pass
    #def visit_word_part(self, node): pass
    #def visit_ArrayLiteralPart(self, node): pass
    def visit_LiteralPart(self, node): self.visit(node.token)
    #def visit_EscapedLiteralPart(self, node): pass
    #def visit_SingleQuotedPart(self, node): pass
    def visit_DoubleQuotedPart(self, node):
        self.visitattr(node, 'parts')
    def visit_SimpleVarSub(self, node): pass
    #def visit_BracedVarSub(self, node): pass
    def visit_TildeSubPart(self, node):
        self.visit(node.token)
    def visit_CommandSubPart(self, node):
        self.visit(node.command_list)
        self.visit(node.left_token)
    #def visit_ArithSubPart(self, node): pass
    #def visit_BracedAltPart(self, node): pass
    #def visit_BracedIntRangePart(self, node): pass
    #def visit_BracedCharRangePart(self, node): pass
    #def visit_ExtGlobPart(self, node): pass
    #def visit_word_e(self, node): pass
    #def visit_word(self, node): pass
    def visit_EmptyWord(self, node): pass
    #def visit_TokenWord(self, node): pass
    def visit_CompoundWord(self, node): self.visitattr(node, 'parts')
    def visit_BracedWordTree(self, node): self.visitattr(node, 'parts')
    #def visit_StringWord(self, node): pass
    #def visit_lhs_expr_e(self, node): pass
    #def visit_lhs_expr(self, node): pass
    def visit_LhsName(self, node): pass
    def visit_LhsIndexedName(self, node): pass
    #def visit_arith_expr_e(self, node): pass
    #def visit_arith_expr(self, node): pass
    #def visit_ArithVarRef(self, node): pass
    #def visit_ArithWord(self, node): pass
    #def visit_UnaryAssign(self, node): pass
    #def visit_BinaryAssign(self, node): pass
    #def visit_ArithUnary(self, node): pass
    #def visit_ArithBinary(self, node): pass
    #def visit_TernaryOp(self, node): pass
    #def visit_FuncCall(self, node): pass
    #def visit_bool_expr_e(self, node): pass
    #def visit_bool_expr(self, node): pass
    #def visit_WordTest(self, node): pass
    #def visit_BoolBinary(self, node): pass
    #def visit_BoolUnary(self, node): pass
    #def visit_LogicalNot(self, node): pass
    #def visit_LogicalAnd(self, node): pass
    #def visit_LogicalOr(self, node): pass
    #def visit_redir_e(self, node): pass
    #def visit_redir(self, node): pass
    #def visit_Redir(self, node): pass
    #def visit_HereDoc(self, node): pass
    #def visit_assign_op_e(self, node): pass
    def visit_assign_pair(self, node):
        self.visit(node.lhs)
        self.visit(node.rhs)
    #def visit_env_pair(self, node): pass
    #def visit_case_arm(self, node): pass
    #def visit_if_arm(self, node): pass
    #def visit_iterable_e(self, node): pass
    #def visit_iterable(self, node): pass
    #def visit_IterArgv(self, node): pass
    #def visit_IterArray(self, node): pass
    #def visit_command_e(self, node): pass
    #def visit_command(self, node): pass
    #def visit_NoOp(self, node): pass
    def visit_SimpleCommand(self, node): self.visitattr(node, 'words')
    def visit_Sentence(self, node):
        self.visit(node.child)
        self.visit(node.terminator)
    def visit_Assignment(self, node): self.visitattr(node, 'pairs')
    def visit_ControlFlow(self, node):
        pass #self.visit(token)
    def visit_Pipeline(self, node):
        self.visitattr(node, 'children')
    def visit_AndOr(self, node): self.visitattr(node, 'children')
    #def visit_DoGroup(self, node): pass
    def visit_BraceGroup(self, node):
        self.visitattr(node, 'children')
        self.visitattr(node, 'redirects')

    #def visit_Subshell(self, node): pass
    #def visit_DParen(self, node): pass
    #def visit_DBracket(self, node): pass
    #def visit_ForEach(self, node): pass
    #def visit_ForExpr(self, node): pass
    #def visit_WhileUntil(self, node): pass
    #def visit_If(self, node): pass
    def visit_Case(self, node):
        self.visitattr(node, 'arms')
        self.visitattr(node, 'redirects')
    def visit_FuncDef(self, node):
        self.visit(node.body)
        self.visitattr(node, 'redirects')

    #def visit_TimeBlock(self, node): pass
    def visit_CommandList(self, node): self.visitattr(node, 'children')
    #def visit_glob_part_e(self, node): pass
    #def visit_glob_part(self, node): pass
    #def visit_GlobLit(self, node): pass
    #def visit_GlobOp(self, node): pass
    #def visit_CharClass(self, node): pass


class VarNameVisitor(AstVisitor):

    """
    XXX: retrieve variable names from AST.
    Scan for names of variable. Default to filter out local vars.
    Switch to include or show ony local. Will take some effort.
    """

class CmdNameVisitor(AstVisitor):

    """
    Retrieve command or variable names from the AST. The basic heuristic is
    simple, retrieve the first literal token of the command list.

    Dynamic command names with multipart, variable tokens cannot be handled
    here.

    That leaves heuristics to deal with certain command constructs not expressed
    in the AST: command prefixing (e.g. sudo, time) (Which leads back to
    the 'eval' prefix also). (env-var prefixes to a command are covered
    by SimpleCommand.more_env)

    Without going into too much detals, these are the modes for CmdNameVisitor:

    - literal command names
    - literal command names following known prefix command
    - variable command names, either all or those matching regex
    """

    prefix = 'print_'
    prefixes = "sudo time eval".split(' ')
    builtins = "test set case if while read exec eval local export return "\
            "continue echo printf which command".split(' ')
    vars = []

    def __init__(self, ignores=None, prefixes=None, vars=None):
        AstVisitor.__init__(self, True, 'print_cmdname_')
        if prefixes:
            self.prefixes = prefixes
        if vars:
            self.vars = vars
        if ignores:
            self.builtins.extend(ignores)

    def print_cmdname_SimpleCommand(self, node):
        """
        Look at first word, if literal token compare to cmd name lists.
        """
        words = node.words[:]
        if words[0].__class__.__name__ in ( 'CompoundWord', ):
            execname = self.getexec_SimpleCommand_CompoundWord(words[0])
            while execname in self.prefixes:
                words.pop(0)
                execname = self.getexec_SimpleCommand_CompoundWord(words[0])
            if not execname or execname in self.builtins:
                return
            if execname.startswith('$'):
                if self.vars:
                    for var_re in self.vars:
                        if re.match(var_re, execname[1:]):
                            print(execname)
                            return
                return
            print(execname)

        else:
            assert False, node

    def getexec_SimpleCommand_CompoundWord(self, node):
        nc = node.parts[0].__class__.__name__

        if nc in (
            'LiteralPart',
            'SimpleVarSub',
            'BracedVarSub'
        ):
            if len(node.parts) > 1:
                # NOTE: ignore multi bits, just visit single command words
                return
            name = node.parts[0].token.val
            if nc == 'BracedVarSub':
                name = '$'+name
            return name

        elif nc in (
            'CommandSubPart',
        ):
            if node.parts[0].command_list.children[0].__class__.__name__ in ('SimpleCommand',):
                pass # self.print_SimpleCommand(node.parts[0].command_list.children[0])
            assert False, node

        elif nc in (
            'DoubleQuotedPart',
        ):
            name = node.parts[0].parts[0].token.val
            if node.parts[0].parts[0].token.id == osh.meta.Id.Lit_Chars:
                print(name, '$')
                return '$'+name
            return name

        elif nc in (
            'TildeSubPart',
        ):
            return ''.join(map(lambda n: n.token.val, node.parts))

        else:
            assert False, node
