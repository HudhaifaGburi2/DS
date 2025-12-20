"""
Scene 02: Mutex Basic Operation
===============================

Shows how mutex solves the race condition:
- Lock before critical section
- Only one thread can hold the lock
- Unlock after critical section

Narrative: Same scenario, but now protected by mutex.
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from config import C, T, F, L, A, OS
from base_scenes import ConcurrencyScene
from components.threads import Thread
from components.locks import Mutex, LockQueue
from components.critical_sections import SharedResource, CriticalSection
from components.effects import LockAcquireEffect, BlockedIndicator
from utils.text_helpers import create_bilingual


class Scene02_MutexBasic(ConcurrencyScene):
    """
    Demonstrates mutex lock/unlock mechanism.
    
    Visual: Lock icon, threads acquiring/releasing,
    queue of waiting threads.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        self.create_title_card(
            "القفل المتبادل",
            "Mutex: Mutual Exclusion"
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: INTRODUCE MUTEX
        # ══════════════════════════════════════════════════════════════════════
        
        section = self.create_section_header("The Mutex Lock")
        self.play(Write(section))
        
        # Create mutex
        mutex = Mutex(label="mutex")
        mutex.scale(1.5)
        mutex.move_to(UP * 0.5)
        
        self.play(FadeIn(mutex, scale=0.8))
        self.wait_beat()
        
        # Explain states
        state_free = Text("🔓 FREE: Any thread can acquire", font=F.CODE, color=C.LOCK_FREE).scale(F.SIZE_LABEL)
        state_held = Text("🔒 HELD: Only holder can release", font=F.CODE, color=C.LOCK_HELD).scale(F.SIZE_LABEL)
        
        states = VGroup(state_free, state_held)
        states.arrange(DOWN, buff=L.SPACING_SM, aligned_edge=LEFT)
        states.shift(DOWN * 1.5)
        
        self.play(Write(state_free))
        self.wait_beat()
        self.play(Write(state_held))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: SETUP PROTECTED SCENARIO
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        # Critical section
        critical = CriticalSection(label="Critical Section", width=3.5, height=2.0)
        critical.move_to(RIGHT * 1.5)
        
        # Shared counter inside
        counter = SharedResource(name="counter", initial_value="0")
        counter.scale(0.8)
        counter.move_to(critical.background.get_center())
        
        # Mutex guarding the section
        mutex = Mutex(label="lock")
        mutex.move_to(LEFT * 2)
        
        # Two threads
        thread1 = Thread(thread_id=1)
        thread2 = Thread(thread_id=2)
        
        thread1.move_to(LEFT * 5 + UP * 1)
        thread2.move_to(LEFT * 5 + DOWN * 1)
        
        self.play(
            FadeIn(critical),
            FadeIn(counter),
            FadeIn(mutex)
        )
        self.play(
            thread1.animate_spawn(),
            thread2.animate_spawn()
        )
        self.wait_beat()
        
        # Labels
        t1_label = Text("T1", font=F.CODE, color=C.THREAD_1).scale(F.SIZE_TINY)
        t1_label.add_updater(lambda m: m.next_to(thread1, UP, buff=0.1))
        
        t2_label = Text("T2", font=F.CODE, color=C.THREAD_2).scale(F.SIZE_TINY)
        t2_label.add_updater(lambda m: m.next_to(thread2, UP, buff=0.1))
        
        self.add(t1_label, t2_label)
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: T1 ACQUIRES LOCK
        # ══════════════════════════════════════════════════════════════════════
        
        step_label = Text("T1: lock()", font=F.CODE, color=C.THREAD_1).scale(F.SIZE_CAPTION)
        step_label.to_edge(UP, buff=L.MARGIN_SM)
        
        self.play(Write(step_label))
        
        # T1 approaches lock
        self.play(thread1.animate.move_to(mutex.get_left() + LEFT * 0.5))
        
        # T1 acquires lock
        self.play(mutex.animate_acquire(1))
        self.play(Flash(mutex, color=C.THREAD_1, line_length=0.2))
        
        # T1 enters critical section
        self.play(thread1.animate.move_to(critical.background.get_center() + UP * 0.3))
        self.play(critical.background.animate.set_fill(color=C.THREAD_1, opacity=0.15))
        
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: T2 TRIES TO ACQUIRE - BLOCKED
        # ══════════════════════════════════════════════════════════════════════
        
        step_label2 = Text("T2: lock() → BLOCKED", font=F.CODE, color=C.THREAD_2).scale(F.SIZE_CAPTION)
        step_label2.to_edge(UP, buff=L.MARGIN_SM)
        
        self.play(Transform(step_label, step_label2))
        
        # T2 approaches lock
        self.play(thread2.animate.move_to(mutex.get_left() + LEFT * 0.5 + DOWN * 0.3))
        
        # T2 tries to acquire - blocked!
        self.play(mutex.animate_contention())
        
        # Show blocked state
        thread2.set_state("blocked")
        blocked_indicator = BlockedIndicator(thread2)
        blocked_indicator.move_to(thread2.get_center() + UP * 0.5)
        
        self.play(
            thread2.body.animate.set_fill(opacity=A.BLOCKED_OPACITY),
            FadeIn(blocked_indicator)
        )
        
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 6: T1 DOES WORK AND RELEASES
        # ══════════════════════════════════════════════════════════════════════
        
        step_label3 = Text("T1: counter++ then unlock()", font=F.CODE, color=C.THREAD_1).scale(F.SIZE_CAPTION)
        step_label3.to_edge(UP, buff=L.MARGIN_SM)
        
        self.play(Transform(step_label, step_label3))
        
        # T1 increments counter
        self.play(counter.animate_write("1", C.THREAD_1))
        self.wait_beat()
        
        # T1 exits and releases lock
        self.play(thread1.animate.move_to(RIGHT * 4 + UP * 1))
        self.play(mutex.animate_release())
        self.play(critical.background.animate.set_fill(color=C.CRITICAL_SECTION, opacity=0.12))
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 7: T2 WAKES AND ACQUIRES
        # ══════════════════════════════════════════════════════════════════════
        
        step_label4 = Text("T2: wakes up, acquires lock", font=F.CODE, color=C.THREAD_2).scale(F.SIZE_CAPTION)
        step_label4.to_edge(UP, buff=L.MARGIN_SM)
        
        self.play(Transform(step_label, step_label4))
        
        # T2 wakes up
        self.play(
            FadeOut(blocked_indicator),
            thread2.body.animate.set_fill(opacity=0.6)
        )
        thread2.set_state("running")
        
        # T2 acquires lock
        self.play(mutex.animate_acquire(2))
        
        # T2 enters critical section
        self.play(thread2.animate.move_to(critical.background.get_center() + DOWN * 0.1))
        self.play(critical.background.animate.set_fill(color=C.THREAD_2, opacity=0.15))
        
        # T2 increments counter
        self.play(counter.animate_write("2", C.THREAD_2))
        
        # T2 exits and releases
        self.play(thread2.animate.move_to(RIGHT * 4 + DOWN * 1))
        self.play(mutex.animate_release())
        self.play(critical.background.animate.set_fill(color=C.CRITICAL_SECTION, opacity=0.12))
        
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 8: SUCCESS!
        # ══════════════════════════════════════════════════════════════════════
        
        success = Text("counter = 2 ✓", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_HEADING)
        success.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(
            FadeIn(success, scale=0.8),
            Flash(counter.container, color=C.SUCCESS, line_length=0.3)
        )
        
        # Explanation
        explanation = create_bilingual(
            "التنفيذ المتسلسل يمنع التنافس",
            "Serialized execution prevents race condition",
            color_ar=C.SUCCESS,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        explanation.next_to(success, UP, buff=L.SPACING_MD)
        
        self.play(FadeIn(explanation))
        self.wait_contemplate()
