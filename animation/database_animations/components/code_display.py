"""
Database Animation Framework - Code Display Components
=======================================================

Syntax-highlighted code blocks and code visualization tools.
"""

from manim import *
import sys
sys.path.append('..')
from config import config, C, T, F, L, A, D


class CodeBlock(VGroup):
    """
    Styled code block with optional syntax highlighting.
    
    Creates a terminal-like display for code snippets.
    """
    
    def __init__(
        self,
        code: str,
        language: str = "python",
        title: str = None,
        width: float = None,
        line_numbers: bool = False,
        highlight_lines: list = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        if width is None:
            width = D.CODE_BOX_WIDTH
        
        self.code_text = code
        self.highlight_lines = highlight_lines or []
        
        # Background box
        lines = code.strip().split('\n')
        height = max(len(lines) * 0.4 + 0.4, D.CODE_BOX_HEIGHT)
        
        self.background = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.15,
            fill_color=C.BACKGROUND_ALT,
            fill_opacity=0.95,
            stroke_color=C.TEXT_TERTIARY,
            stroke_width=1
        )
        
        # Title bar (optional)
        if title:
            self.title_bar = Rectangle(
                width=width,
                height=0.4,
                fill_color="#1a1a2e",
                fill_opacity=1,
                stroke_width=0
            )
            self.title_bar.align_to(self.background, UP)
            self.title_bar.shift(DOWN * 0.2)
            
            self.title_text = Text(
                title,
                font=F.CODE,
                color=C.TEXT_SECONDARY
            ).scale(F.SIZE_LABEL)
            self.title_text.move_to(self.title_bar)
            
            # Window controls (decorative)
            controls = VGroup()
            for i, color in enumerate(["#FF5F56", "#FFBD2E", "#27C93F"]):
                dot = Dot(radius=0.05, color=color)
                dot.shift(LEFT * (1.5 - i * 0.2))
                controls.add(dot)
            controls.move_to(self.title_bar).align_to(self.title_bar, LEFT).shift(RIGHT * 0.3)
            
            self.add(self.title_bar, self.title_text, controls)
        
        # Code content
        self.code_lines = VGroup()
        
        for i, line in enumerate(lines):
            # Line number
            if line_numbers:
                line_num = Text(
                    str(i + 1).rjust(2),
                    font=F.CODE,
                    color=C.TEXT_TERTIARY
                ).scale(F.SIZE_CODE)
                self.code_lines.add(line_num)
            
            # Code text
            if line.strip():
                code_line = self._create_highlighted_line(line, language)
            else:
                code_line = Text(" ", font=F.CODE).scale(F.SIZE_CODE)
            
            self.code_lines.add(code_line)
        
        self.code_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        self.code_lines.move_to(self.background)
        
        if title:
            self.code_lines.shift(DOWN * 0.15)
        
        self.add(self.background, self.code_lines)
    
    def _create_highlighted_line(self, line: str, language: str) -> VGroup:
        """Create syntax-highlighted line of code"""
        # Simple keyword highlighting
        keywords = {
            "python": ["def", "class", "import", "from", "return", "if", "else", "for", "while", "with", "as", "try", "except", "raise"],
            "go": ["func", "package", "import", "return", "if", "else", "for", "range", "defer", "go", "chan", "select", "var", "const", "type", "struct"],
            "c": ["int", "char", "void", "return", "if", "else", "for", "while", "struct", "typedef", "include", "define"],
        }
        
        builtin_funcs = ["print", "open", "close", "write", "read", "len", "range", "os", "rename", "truncate", "fsync"]
        
        line_group = VGroup()
        current_word = ""
        
        # Simple tokenization
        result_text = Text(line, font=F.CODE, color=C.TEXT_CODE).scale(F.SIZE_CODE)
        return result_text
    
    def animate_write(self) -> Succession:
        """Typewriter-style code appearance"""
        return Succession(
            FadeIn(self.background, run_time=T.QUICK),
            Write(self.code_lines, run_time=T.SLOW),
        )
    
    def animate_highlight_line(self, line_index: int, color=None) -> Animation:
        """Highlight a specific line"""
        if color is None:
            color = C.PRIMARY_YELLOW
        
        if 0 <= line_index < len(self.code_lines):
            return Indicate(
                self.code_lines[line_index],
                color=color,
                scale_factor=1.05
            )
        return Wait(0)
    
    def get_line(self, index: int) -> Mobject:
        """Get a specific line for highlighting"""
        if 0 <= index < len(self.code_lines):
            return self.code_lines[index]
        return None


class SyntaxHighlightedCode(VGroup):
    """
    More sophisticated syntax highlighting using Code mobject.
    
    Wraps Manim's Code class with consistent styling.
    """
    
    def __init__(
        self,
        code: str,
        language: str = "python",
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # Use Manim's built-in Code class
        self.code = Code(
            code=code,
            language=language,
            tab_width=4,
            font_size=24,
            background="rectangle",
            background_stroke_color=C.TEXT_TERTIARY,
            background_stroke_width=1,
            insert_line_no=False,
            style="monokai"
        )
        
        self.add(self.code)
    
    def animate_appear(self) -> Animation:
        """Fade in the code block"""
        return FadeIn(self.code, run_time=T.NORMAL)


class CommandPrompt(VGroup):
    """
    Terminal command prompt visualization.
    
    Shows shell commands with $ prefix.
    """
    
    def __init__(
        self,
        command: str,
        output: str = None,
        prompt: str = "$",
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # Prompt
        self.prompt = Text(
            prompt,
            font=F.CODE,
            color=C.SUCCESS
        ).scale(F.SIZE_CODE)
        
        # Command
        self.command = Text(
            command,
            font=F.CODE,
            color=C.TEXT_PRIMARY
        ).scale(F.SIZE_CODE)
        
        self.command.next_to(self.prompt, RIGHT, buff=L.SPACING_SM)
        
        self.add(self.prompt, self.command)
        
        # Output (optional)
        if output:
            self.output = Text(
                output,
                font=F.CODE,
                color=C.TEXT_SECONDARY
            ).scale(F.SIZE_CODE)
            self.output.next_to(VGroup(self.prompt, self.command), DOWN, aligned_edge=LEFT, buff=L.SPACING_SM)
            self.add(self.output)
    
    def animate_type(self) -> Succession:
        """Typewriter effect for command"""
        anims = [
            Write(self.prompt, run_time=T.INSTANT),
            Write(self.command, run_time=T.NORMAL)
        ]
        
        if hasattr(self, 'output'):
            anims.append(FadeIn(self.output, run_time=T.FAST))
        
        return Succession(*anims)


class FunctionSignature(VGroup):
    """
    Highlighted function signature display.
    
    Shows function name with parameters.
    """
    
    def __init__(
        self,
        func_name: str,
        params: list = None,
        return_type: str = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # Function name
        self.func_name = Text(
            func_name,
            font=F.CODE,
            color=C.PRIMARY_YELLOW
        ).scale(F.SIZE_BODY)
        
        parts = [self.func_name]
        
        # Parameters
        if params:
            param_text = "(" + ", ".join(params) + ")"
            self.params = Text(
                param_text,
                font=F.CODE,
                color=C.TEXT_CODE
            ).scale(F.SIZE_BODY)
            self.params.next_to(self.func_name, RIGHT, buff=0.02)
            parts.append(self.params)
        
        # Return type
        if return_type:
            self.return_type = Text(
                f" → {return_type}",
                font=F.CODE,
                color=C.TEXT_SECONDARY
            ).scale(F.SIZE_BODY)
            self.return_type.next_to(parts[-1], RIGHT, buff=0.05)
            parts.append(self.return_type)
        
        for part in parts:
            self.add(part)
