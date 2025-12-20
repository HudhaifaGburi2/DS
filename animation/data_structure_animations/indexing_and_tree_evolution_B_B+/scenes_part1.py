"""
B-Tree Evolution Animation - Scenes A-D
========================================

Part 1: Foundation concepts
- Scene A: Writing Data to Disk
- Scene B: Building the Indexing Table
- Scene C: Index Lookup (Binary Search)
- Scene D: Index Growth Problem
"""

from manim import *
import sys
from pathlib import Path

from config import C, T, S, F, A, L
from components import (
    DiskBlock, DiskSurface, IndexEntry, IndexTable,
    BTreeNode, NarrationBox, MemoryRegion
)


# ══════════════════════════════════════════════════════════════════════════════
# BASE SCENE CLASS
# ══════════════════════════════════════════════════════════════════════════════

class BTreeBaseScene(Scene):
    """Base scene with common utilities"""
    
    def setup(self):
        self.camera.background_color = C.BACKGROUND
    
    def create_title(self, text: str, arabic: str = None):
        """Create scene title"""
        title = Text(text, font=F.MAIN_FONT, font_size=F.TITLE, color=C.TEXT_PRIMARY)
        title.to_edge(UP, buff=0.4)
        
        if arabic:
            arabic_text = Text(arabic, font=F.ARABIC_FONT, font_size=F.HEADING, color=C.TEXT_SECONDARY)
            arabic_text.next_to(title, DOWN, buff=0.15)
            return VGroup(title, arabic_text)
        return title
    
    def narrate(self, *lines, position=DOWN * 3, wait_time=None):
        """Show narration text"""
        narration = VGroup()
        for line in lines:
            text = Text(line, font=F.MAIN_FONT, font_size=F.BODY, color=C.TEXT_NARRATION)
            narration.add(text)
        narration.arrange(DOWN, buff=F.NARRATION_SPACING, aligned_edge=LEFT)
        narration.move_to(position)
        
        # Ensure it fits on screen
        if narration.width > 12:
            narration.scale(12 / narration.width)
        
        anims = [FadeIn(line, shift=UP * 0.2) for line in narration]
        self.play(LaggedStart(*anims, lag_ratio=0.3))
        
        if wait_time:
            self.wait(wait_time)
        else:
            self.wait(len(lines) * T.NARRATION_LINE)
        
        return narration
    
    def scene_transition(self):
        """Fade out all objects"""
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=T.SCENE_TRANSITION)
        self.wait(0.2)


# ══════════════════════════════════════════════════════════════════════════════
# SCENE A — Writing Data to Disk
# ══════════════════════════════════════════════════════════════════════════════

class SceneA_DiskWrite(BTreeBaseScene):
    """
    Animation: How records are written to disk blocks.
    
    Key concepts:
    - Disk storage organized into blocks
    - Multiple records per block
    - Block addressing
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # TITLE
        # ══════════════════════════════════════════════════════════════════════
        title = self.create_title("Writing Data to Disk", "كتابة البيانات إلى القرص")
        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # NARRATION 1: Record insertion
        # ══════════════════════════════════════════════════════════════════════
        narration1 = self.narrate(
            "When a record is inserted into a database,",
            "it is first written to disk."
        )
        self.wait(T.ABSORB)
        self.play(FadeOut(narration1))
        
        # ══════════════════════════════════════════════════════════════════════
        # DISK SURFACE SETUP
        # ══════════════════════════════════════════════════════════════════════
        disk = DiskSurface(num_blocks=4)
        disk.shift(DOWN * 0.5)
        
        self.play(FadeIn(disk, shift=UP * 0.5), run_time=T.NORMAL)
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # NARRATION 2: Block organization
        # ══════════════════════════════════════════════════════════════════════
        narration2 = self.narrate(
            "Disk storage is organized into blocks,",
            "not individual records."
        )
        
        # Highlight blocks
        for block in disk.blocks:
            self.play(
                block.container.animate.set_stroke(color=C.HIGHLIGHT, width=3),
                run_time=T.QUICK
            )
        self.play(
            *[block.container.animate.set_stroke(color=C.DISK_BLOCK, width=2) 
              for block in disk.blocks],
            run_time=T.FAST
        )
        
        self.play(FadeOut(narration2))
        
        # ══════════════════════════════════════════════════════════════════════
        # RECORD INSERTION ANIMATION
        # ══════════════════════════════════════════════════════════════════════
        narration3 = self.narrate(
            "Multiple records are packed",
            "into the same disk block."
        )
        self.play(FadeOut(narration3))
        
        # Records to insert
        records = [
            (101, 0), (205, 0),  # Block 1
            (312, 1), (450, 1),  # Block 2
            (523, 2), (611, 2),  # Block 3
            (720, 3), (835, 3),  # Block 4
        ]
        
        for record_id, block_idx in records:
            # Create record falling from top
            record = Text(
                str(record_id),
                font=F.CODE_FONT,
                font_size=F.DATA_SIZE,
                color=C.DATA
            )
            record.move_to(UP * 3.5)
            
            # Target block
            target_block = disk.blocks[block_idx]
            slot_idx = len(target_block.record_objects)
            
            if slot_idx < target_block.max_records:
                target_pos = target_block.slots[slot_idx].get_center()
                
                self.play(FadeIn(record, scale=0.5))
                self.play(
                    record.animate.move_to(target_pos),
                    target_block.slots[slot_idx].animate.set_fill(color=C.DATA, opacity=A.DIMMED),
                    run_time=T.DISK_WRITE,
                    rate_func=rate_functions.ease_out_bounce
                )
                target_block.record_objects.append(record)
                target_block.add(record)
        
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # BLOCK ADDRESSING
        # ══════════════════════════════════════════════════════════════════════
        narration4 = self.narrate(
            "The database remembers",
            "the block address where each record is stored."
        )
        
        # Highlight block addresses
        for block in disk.blocks:
            self.play(
                block.address_label.animate.set_color(C.POINTER).scale(1.3),
                run_time=T.FAST
            )
        
        self.wait(T.ABSORB)
        
        # Reset
        self.play(
            *[block.address_label.animate.set_color(C.POINTER).scale(1/1.3)
              for block in disk.blocks],
            FadeOut(narration4)
        )
        
        self.wait(T.BEAT)
        self.scene_transition()


# ══════════════════════════════════════════════════════════════════════════════
# SCENE B — Building the Indexing Table
# ══════════════════════════════════════════════════════════════════════════════

class SceneB_IndexTable(BTreeBaseScene):
    """
    Animation: Creating and maintaining an index table.
    
    Key concepts:
    - Index entries with key + pointer
    - Sorted order maintenance
    - Index separate from data
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # TITLE
        # ══════════════════════════════════════════════════════════════════════
        title = self.create_title("Building the Indexing Table", "بناء جدول الفهرسة")
        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # DISK WITH DATA (from previous scene)
        # ══════════════════════════════════════════════════════════════════════
        disk = DiskSurface(num_blocks=3)
        disk.shift(DOWN * 2)
        disk.scale(0.8)
        
        # Pre-populate with records
        records_data = [
            [(100, 0), (200, 0)],
            [(300, 1), (400, 1)],
            [(500, 2), (600, 2)],
        ]
        
        for block_idx, records in enumerate(records_data):
            for rec_id, _ in records:
                rec = Text(str(rec_id), font=F.CODE_FONT, font_size=14, color=C.DATA)
                slot_idx = len(disk.blocks[block_idx].record_objects)
                rec.move_to(disk.blocks[block_idx].slots[slot_idx].get_center())
                disk.blocks[block_idx].record_objects.append(rec)
                disk.blocks[block_idx].add(rec)
        
        self.play(FadeIn(disk))
        
        # ══════════════════════════════════════════════════════════════════════
        # NARRATION: Index introduction
        # ══════════════════════════════════════════════════════════════════════
        narration1 = self.narrate(
            "Alongside the data file,",
            "the database builds an indexing table."
        )
        self.play(FadeOut(narration1))
        
        # ══════════════════════════════════════════════════════════════════════
        # INDEX TABLE CREATION
        # ══════════════════════════════════════════════════════════════════════
        
        # Table header
        header = VGroup(
            Text("Key", font=F.MAIN_FONT, font_size=F.LABEL, color=C.KEY),
            Text("Block", font=F.MAIN_FONT, font_size=F.LABEL, color=C.POINTER)
        )
        header.arrange(RIGHT, buff=1.2)
        header.shift(UP * 2)
        
        self.play(Write(header))
        
        # Create index entries
        index_data = [
            (100, 1), (200, 1),
            (300, 2), (400, 2),
            (500, 3), (600, 3),
        ]
        
        entries = VGroup()
        for i, (key, block) in enumerate(index_data):
            entry = IndexEntry(key, block)
            entry.scale(0.85)
            entry.shift(UP * (1.3 - i * 0.55))
            entries.add(entry)
        
        # Animate entries appearing
        self.play(
            LaggedStart(*[FadeIn(e, shift=LEFT * 0.3) for e in entries], lag_ratio=0.15)
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # NARRATION: Index structure
        # ══════════════════════════════════════════════════════════════════════
        narration2 = self.narrate(
            "Each index entry contains:",
            "a search key, and a pointer to a disk block."
        )
        
        # Highlight key column
        self.play(
            *[e.key_cell.animate.set_stroke(color=C.KEY, width=3) for e in entries],
            run_time=T.FAST
        )
        self.wait(T.BEAT)
        
        # Highlight pointer column
        self.play(
            *[e.ptr_cell.animate.set_stroke(color=C.POINTER, width=3) for e in entries],
            run_time=T.FAST
        )
        
        self.play(FadeOut(narration2))
        
        # Reset highlights
        self.play(
            *[e.key_cell.animate.set_stroke(color=C.KEY, width=1) for e in entries],
            *[e.ptr_cell.animate.set_stroke(color=C.POINTER, width=1) for e in entries],
            run_time=T.FAST
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # SORTED ORDER
        # ══════════════════════════════════════════════════════════════════════
        narration3 = self.narrate(
            "The index is always kept sorted by key."
        )
        
        # Highlight sorted order (keys glowing in sequence)
        for entry in entries:
            self.play(
                entry.key_text.animate.set_color(C.SUCCESS).scale(1.15),
                run_time=T.QUICK
            )
            self.play(
                entry.key_text.animate.set_color(C.KEY).scale(1/1.15),
                run_time=T.QUICK
            )
        
        self.wait(T.ABSORB)
        self.play(FadeOut(narration3))
        self.scene_transition()


# ══════════════════════════════════════════════════════════════════════════════
# SCENE C — Index Lookup (Binary Search)
# ══════════════════════════════════════════════════════════════════════════════

class SceneC_BinarySearch(BTreeBaseScene):
    """
    Animation: Binary search through index.
    
    Key concepts:
    - Binary search algorithm
    - Pointer dereference
    - Single disk read result
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # TITLE
        # ══════════════════════════════════════════════════════════════════════
        title = self.create_title("Index Lookup: Binary Search", "البحث في الفهرس")
        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # SETUP INDEX AND DISK
        # ══════════════════════════════════════════════════════════════════════
        
        # Index entries (sorted)
        index_keys = [100, 200, 300, 400, 500, 600, 700, 800]
        entries = VGroup()
        
        for i, key in enumerate(index_keys):
            entry = IndexEntry(key, (i // 2) + 1)
            entry.scale(0.75)
            entry.shift(LEFT * 4 + UP * (2 - i * 0.5))
            entries.add(entry)
        
        # Disk blocks
        disk_blocks = VGroup()
        for i in range(4):
            block = DiskBlock(i + 1)
            block.scale(0.7)
            block.shift(RIGHT * 3 + UP * (1.5 - i * 1.2))
            disk_blocks.add(block)
        
        self.play(FadeIn(entries), FadeIn(disk_blocks))
        
        # ══════════════════════════════════════════════════════════════════════
        # NARRATION: Search approach
        # ══════════════════════════════════════════════════════════════════════
        narration1 = self.narrate(
            "To find a record, the database searches the index.",
            "Because the index is sorted, binary search can be used."
        )
        self.play(FadeOut(narration1))
        
        # ══════════════════════════════════════════════════════════════════════
        # SEARCH QUERY
        # ══════════════════════════════════════════════════════════════════════
        search_target = 500
        query_box = VGroup(
            Text("Search:", font=F.MAIN_FONT, font_size=F.LABEL, color=C.TEXT_SECONDARY),
            Text(str(search_target), font=F.CODE_FONT, font_size=F.HEADING, color=C.SELECTED)
        )
        query_box.arrange(RIGHT, buff=0.3)
        query_box.to_corner(UR, buff=0.5)
        
        self.play(FadeIn(query_box, scale=0.8))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # BINARY SEARCH ANIMATION
        # ══════════════════════════════════════════════════════════════════════
        
        low, high = 0, len(index_keys) - 1
        
        while low <= high:
            mid = (low + high) // 2
            
            # Highlight search range
            range_box = SurroundingRectangle(
                VGroup(*entries[low:high+1]),
                color=C.SEARCH_PATH,
                buff=0.1,
                stroke_width=2
            )
            self.play(Create(range_box), run_time=T.FAST)
            
            # Highlight middle element
            mid_entry = entries[mid]
            self.play(
                mid_entry.key_cell.animate.set_fill(color=C.SELECTED, opacity=A.NORMAL),
                mid_entry.key_text.animate.set_color(WHITE).scale(1.2),
                run_time=T.SEARCH_STEP
            )
            
            # Compare indicator
            compare_text = Text(
                f"{index_keys[mid]} {'=' if index_keys[mid] == search_target else '<' if index_keys[mid] < search_target else '>'} {search_target}",
                font=F.CODE_FONT,
                font_size=F.LABEL,
                color=C.TEXT_ACCENT
            )
            compare_text.next_to(mid_entry, RIGHT, buff=0.5)
            self.play(FadeIn(compare_text))
            self.wait(T.BEAT)
            
            if index_keys[mid] == search_target:
                # Found!
                self.play(
                    mid_entry.key_cell.animate.set_fill(color=C.SUCCESS, opacity=A.NORMAL),
                    FadeOut(compare_text),
                    FadeOut(range_box)
                )
                break
            elif index_keys[mid] < search_target:
                low = mid + 1
            else:
                high = mid - 1
            
            # Reset and continue
            self.play(
                mid_entry.key_cell.animate.set_fill(color=C.KEY, opacity=A.FADED),
                mid_entry.key_text.animate.set_color(C.KEY).scale(1/1.2),
                FadeOut(compare_text),
                FadeOut(range_box),
                run_time=T.FAST
            )
        
        # ══════════════════════════════════════════════════════════════════════
        # POINTER JUMP
        # ══════════════════════════════════════════════════════════════════════
        narration2 = self.narrate(
            "Once the key is found,",
            "the pointer jumps directly to the correct disk block."
        )
        self.play(FadeOut(narration2))
        
        # Find which block
        found_entry = entries[4]  # Key 500
        target_block = disk_blocks[2]  # Block 3
        
        # Animate pointer jump
        pointer_arrow = Arrow(
            found_entry.ptr_cell.get_right(),
            target_block.container.get_left(),
            color=C.POINTER,
            stroke_width=S.ARROW_STROKE,
            buff=0.1
        )
        
        self.play(GrowArrow(pointer_arrow), run_time=T.NORMAL)
        self.play(
            target_block.container.animate.set_stroke(color=C.SUCCESS, width=4),
            Flash(target_block.container, color=C.SUCCESS, line_length=0.3)
        )
        
        # Disk read counter
        read_counter = VGroup(
            Text("Disk Reads:", font=F.MAIN_FONT, font_size=F.LABEL, color=C.TEXT_SECONDARY),
            Text("1", font=F.CODE_FONT, font_size=F.HEADING, color=C.SUCCESS)
        )
        read_counter.arrange(RIGHT, buff=0.3)
        read_counter.to_corner(DR, buff=0.5)
        
        self.play(FadeIn(read_counter, scale=0.8))
        self.wait(T.CONTEMPLATE)
        
        self.scene_transition()


# ══════════════════════════════════════════════════════════════════════════════
# SCENE D — Index Growth Problem
# ══════════════════════════════════════════════════════════════════════════════

class SceneD_IndexGrowth(BTreeBaseScene):
    """
    Animation: Index outgrowing memory.
    
    Key concepts:
    - Index size growth
    - Memory limitations
    - Disk I/O penalty
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # TITLE
        # ══════════════════════════════════════════════════════════════════════
        title = self.create_title("Index Growth Problem", "مشكلة نمو الفهرس")
        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # MEMORY/DISK BOUNDARY
        # ══════════════════════════════════════════════════════════════════════
        memory_line = Line(LEFT * 6.5, RIGHT * 6.5, color=C.MEMORY, stroke_width=3)
        memory_line.shift(UP * 0.3)
        
        memory_label = Text("MEMORY", font=F.MAIN_FONT, font_size=F.LABEL, color=C.MEMORY)
        memory_label.next_to(memory_line, UL, buff=0.1)
        
        disk_label = Text("DISK", font=F.MAIN_FONT, font_size=F.LABEL, color=C.DISK_BLOCK)
        disk_label.next_to(memory_line, DL, buff=0.1)
        
        self.play(Create(memory_line), Write(memory_label), Write(disk_label))
        
        # ══════════════════════════════════════════════════════════════════════
        # SMALL INDEX IN MEMORY
        # ══════════════════════════════════════════════════════════════════════
        index_box = RoundedRectangle(
            width=2.5, height=1.5,
            color=C.SUCCESS,
            fill_opacity=A.DIMMED,
            corner_radius=0.1
        )
        index_box.shift(UP * 1.8)
        
        index_label = Text("Index", font=F.MAIN_FONT, font_size=F.LABEL, color=C.SUCCESS)
        index_label.move_to(index_box)
        
        self.play(FadeIn(VGroup(index_box, index_label)))
        
        narration1 = self.narrate(
            "As data grows,",
            "the index grows with it."
        )
        self.play(FadeOut(narration1))
        
        # ══════════════════════════════════════════════════════════════════════
        # INDEX GROWTH ANIMATION
        # ══════════════════════════════════════════════════════════════════════
        
        # Grow index progressively
        for scale_factor in [1.3, 1.6, 2.0, 2.5]:
            self.play(
                index_box.animate.scale(scale_factor / (scale_factor / 1.3 if scale_factor > 1.3 else 1)),
                run_time=T.NORMAL
            )
            
            # Warning when approaching boundary
            if scale_factor >= 2.0:
                index_box.set_color(C.WARNING)
                index_label.set_color(C.WARNING)
        
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # INDEX MOVES TO DISK
        # ══════════════════════════════════════════════════════════════════════
        narration2 = self.narrate(
            "Eventually, the index no longer fits in memory.",
            "Now the index must be read from disk."
        )
        self.play(FadeOut(narration2))
        
        # Move index below memory line
        self.play(
            index_box.animate.shift(DOWN * 2.5).set_color(C.ERROR),
            index_label.animate.shift(DOWN * 2.5).set_color(C.ERROR),
            run_time=T.SLOW
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # PROBLEM INDICATION
        # ══════════════════════════════════════════════════════════════════════
        narration3 = self.narrate(
            "We are back to the same problem:",
            "too many disk accesses."
        )
        
        # Warning indicator
        warning = Text(
            "⚠ Multiple Disk I/Os Required!",
            font=F.MAIN_FONT,
            font_size=F.SUBHEADING,
            color=C.ERROR
        )
        warning.next_to(index_box, RIGHT, buff=0.5)
        
        self.play(FadeIn(warning, scale=1.2))
        self.play(
            Flash(index_box, color=C.ERROR, line_length=0.4),
            index_box.animate.set_stroke(width=4)
        )
        
        # I/O counter increasing
        io_counter = VGroup(
            Text("Disk I/Os:", font=F.MAIN_FONT, font_size=F.LABEL, color=C.TEXT_SECONDARY),
            Text("1", font=F.CODE_FONT, font_size=F.HEADING, color=C.ERROR)
        )
        io_counter.arrange(RIGHT, buff=0.2)
        io_counter.to_corner(DR, buff=0.5)
        
        self.play(FadeIn(io_counter))
        
        for count in [2, 3, 5, 8]:
            new_count = Text(str(count), font=F.CODE_FONT, font_size=F.HEADING, color=C.ERROR)
            new_count.move_to(io_counter[1])
            self.play(Transform(io_counter[1], new_count), run_time=T.FAST)
            self.wait(0.2)
        
        self.wait(T.CONTEMPLATE)
        self.play(FadeOut(narration3))
        self.scene_transition()
