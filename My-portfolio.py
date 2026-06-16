import asyncio
import sys
import os
import json
import base64
import webbrowser
from datetime import datetime
from urllib.parse import quote

import flet
from flet import (
    AppBar, Page, Container, Column, Row, Text, TextField, Button,
    ButtonStyle, TextStyle,
    Tab, Tabs, TabBar, TabBarView, TabAlignment, ListView, IconButton,
    Card, Icon, Divider, Checkbox, Image,
    icons, Colors, border_radius, Padding, Border, MainAxisAlignment, CrossAxisAlignment,
    ClipBehavior
)
from flet_video import Video, VideoMedia

# ============================================================================
# PROFESSIONAL COLOR SCHEME - Modern Dark with Professional Accents
# ============================================================================
BG_MAIN = "#0A0E27"                 # Deep navy-black
BG_SECONDARY = "#F8F9FC"            # Clean white
ACCENT_PRIMARY = "#1A202C"          # Dark charcoal
ACCENT_SECONDARY = "#2563EB"        # Professional blue
SUCCESS = "#059669"                 # Emerald green
TEXT_PRIMARY = "#FFFFFF"            # Pure white
TEXT_SECONDARY = "#E0E7FF"          # Light lavender
TEXT_LIGHT = "#94A3B8"              # Medium gray
CARD_BG = "#FFFFFF"                 # Clean white cards
BORDER_COLOR = "#E2E8F0"            # Light border
ACCENT_CYAN = "#0891B2"             # Cyan accent
FOOTER_BG = "#0F172A"               # Darker footer
HOVER_COLOR = "#3B82F6"             # Lighter blue for hover

VIEW_ONLY = False
EDITOR_EMAIL = "gerhardmangundu@gmail.com"
REQUEST_SUBJECT = "Request Edit Access to Portfolio"
REQUEST_BODY = "Hello,%0D%0A%0D%0APlease grant me edit access to the portfolio.%0D%0A%0D%0AThanks.%0D%0A"


def suppress_windows_connection_reset_noise():
    """Hide harmless Windows asyncio disconnect noise from Flet web sessions."""
    if sys.platform != "win32":
        return

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return

    def handle_exception(loop, context):
        exception = context.get("exception")
        handle = str(context.get("handle", ""))
        if (
            isinstance(exception, ConnectionResetError)
            and getattr(exception, "winerror", None) == 10054
            and "_ProactorBasePipeTransport._call_connection_lost" in handle
        ):
            return
        loop.default_exception_handler(context)

    loop.set_exception_handler(handle_exception)


def run_portfolio_app():
    suppress_windows_connection_reset_noise()
    flet.run(
        main,
        before_main=lambda page: suppress_windows_connection_reset_noise(),
        view=flet.AppView.WEB_BROWSER,
        assets_dir="assets",
        port=8550,
    )


# ============================================================================
# LANDING PAGE
# ============================================================================
def build_landing_page(on_nav):
    """Landing page with profile, introduction, and quick highlights."""
    image_path = os.path.join(os.path.dirname(__file__), "WhatsApp Image 2026-06-13 at 20.14.05.jpeg")
    image_src = None
    
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("ascii")
                image_src = f"data:image/jpeg;base64,{encoded}"
    except Exception:
        image_src = None

    highlights = [
        ("01", "Group 10", "Mining project team contribution."),
        ("02", "Blast Master Pro", "App work, backend flow, and evidence."),
        ("03", "Firebase Lead", "Authentication, database, and cloud setup."),
        ("04", "Reflection", "Progress, learning, and final review."),
    ]

    return Container(
        bgcolor=BG_MAIN,
        content=Column(
            spacing=0,
            scroll="auto",
            controls=[
                Container(
                    padding=Padding.symmetric(vertical=60, horizontal=48),
                    bgcolor=BG_MAIN,
                    content=Row(
                        alignment="space_between",
                        vertical_alignment="center",
                        spacing=48,
                        controls=[
                            Column(
                                expand=True,
                                spacing=24,
                                controls=[
                                    Text("Gerhard Mangundu", size=48, weight="bold", color=Colors.WHITE),
                                    Text(
                                        "Firebase Lead — Group 10 — Blast Master Pro",
                                        size=18,
                                        color=ACCENT_SECONDARY,
                                        weight="600",
                                    ),
                                    Divider(color=ACCENT_SECONDARY, height=2),
                                    Text(
                                        "This portfolio presents my contribution to the Mining Project for Blast Master Pro. "
                                        "I led the Firebase infrastructure, managing cloud services, authentication systems, "
                                        "database architecture, and backend connectivity to ensure reliable app performance.",
                                        size=16,
                                        color=TEXT_SECONDARY,
                                        weight="400",
                                    ),
                                    Button(
                                        "View Project Timeline",
                                        width=240,
                                        height=52,
                                        bgcolor=ACCENT_SECONDARY,
                                        color=Colors.WHITE,
                                        style=ButtonStyle(text_style=TextStyle(size=15, weight="bold")),
                                        on_click=lambda e: on_nav(1),
                                    ),
                                ],
                            ),
                            Container(
                                width=360,
                                height=360,
                                border_radius=12,
                                bgcolor=ACCENT_PRIMARY,
                                border=Border.all(2, ACCENT_SECONDARY),
                                clip_behavior=ClipBehavior.HARD_EDGE,
                                content=Image(src=image_src or "", fit="cover", expand=True),
                            ),
                        ],
                    ),
                ),
                Container(
                    padding=Padding.symmetric(vertical=40, horizontal=48),
                    bgcolor=BG_MAIN,
                    content=Column(
                        spacing=24,
                        controls=[
                            Text("Key Highlights", size=24, weight="bold", color=Colors.WHITE),
                            Row(
                                spacing=18,
                                wrap=True,
                                controls=[
                                    Container(
                                        expand=True,
                                        padding=24,
                                        border_radius=8,
                                        bgcolor=CARD_BG,
                                        border=Border.all(1, BORDER_COLOR),
                                        content=Column(
                                            spacing=12,
                                            controls=[
                                                Container(
                                                    padding=12,
                                                    border_radius=6,
                                                    bgcolor=ACCENT_SECONDARY,
                                                    content=Text(
                                                        number,
                                                        size=24,
                                                        weight="bold",
                                                        color=Colors.WHITE,
                                                        text_align="center",
                                                    )
                                                ),
                                                Text(title, size=16, color=ACCENT_PRIMARY, weight="bold"),
                                                Text(body, size=13, color=TEXT_LIGHT),
                                            ],
                                        ),
                                    )
                                    for number, title, body in highlights
                                ],
                            ),
                        ]
                    ),
                ),
                build_footer(),
            ],
        ),
        expand=True,
    )


# ============================================================================
# FOOTER COMPONENT
# ============================================================================
def build_footer():
    """Reusable footer for all pages"""
    return Container(
        bgcolor=FOOTER_BG,
        padding=32,
        content=Column(
            spacing=16,
            controls=[
                Divider(color=Colors.WHITE10, height=1),
                Row(
                    alignment="space_between",
                    controls=[
                        Column(
                            spacing=8,
                            controls=[
                                Text("Gerhard Mangundu | Portfolio", size=13, weight="bold", color=Colors.WHITE),
                                Text("Firebase Lead & Project Developer", size=12, color=Colors.WHITE60),
                            ]
                        ),
                        Column(
                            spacing=8,
                            horizontal_alignment="end",
                            controls=[
                                Text(f"© {datetime.now().year} Gerhard Mangundu. All rights reserved.", 
                                     size=12, color=Colors.WHITE60),
                                Text("Group 10 - Blast Master Pro", size=12, color=ACCENT_SECONDARY),
                            ]
                        ),
                    ]
                ),
            ]
        )
    )


def status_badge(is_complete: bool, label: str = ""):
    """Status badge component"""
    if is_complete:
        return Row(
            spacing=6,
            controls=[
                Icon(flet.Icons.CHECK_CIRCLE, color=SUCCESS, size=18),
                Text("Complete", size=12, color=SUCCESS, weight="bold")
            ]
        )
    else:
        status_text = label or "View Details"
        return Row(
            spacing=6,
            controls=[
                Icon(flet.Icons.INFO, color=ACCENT_SECONDARY, size=18),
                Text(status_text, size=12, color=ACCENT_SECONDARY, weight="bold")
            ]
        )


# ============================================================================
# SECTION 1: PROJECT TIMELINE
# ============================================================================
def build_timeline_section():
    """Frontend work timeline with a visual progress rail."""
    
    default_entries = [
        {
            "week": "1",
            "milestone": "Planning Sprint - Mapped the first screen ideas and user paths",
            "details": "Outlined the main pages, sketched early flows, and clarified what each screen needed to help users complete tasks.",
            "type": "Design"
        },
        {
            "week": "2",
            "milestone": "Visual Direction - Set a consistent identity for the project",
            "details": "Explored logo options, chose a practical visual direction, and aligned colors and spacing for a cleaner interface.",
            "type": "Branding"
        },
        {
            "week": "3",
            "milestone": "Screen Drafts - Refined dashboard and profile layouts",
            "details": "Turned the early sketches into polished mockups with clearer hierarchy, stronger spacing, and responsive layout choices.",
            "type": "Design"
        },
        {
            "week": "4",
            "milestone": "App Build - Converted the designs into Flet screens",
            "details": "Built the main pages with Flet components, structured the navigation, and styled the interface to match the project direction.",
            "type": "Development"
        },
        {
            "week": "5",
            "milestone": "Interface Polish - Improved spacing, contrast, and feedback",
            "details": "Adjusted typography, card spacing, colors, and feedback states so the app felt more consistent across screen sizes.",
            "type": "Development"
        },
        {
            "week": "6",
            "milestone": "Interaction Pass - Strengthened navigation and form behavior",
            "details": "Added validation, clearer navigation behavior, and user feedback so the interface responded more predictably.",
            "type": "Development"
        },
    ]
    
    timeline_file = os.path.join(os.path.dirname(__file__), "timeline.json")
    
    def load_timeline():
        if os.path.exists(timeline_file):
            try:
                with open(timeline_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return default_entries
        return default_entries
    
    entries = load_timeline()
    timeline_list = ListView(expand=True, spacing=0, padding=Padding.only(bottom=16))
    type_colors = {
        "Design": ACCENT_SECONDARY,
        "Branding": ACCENT_CYAN,
        "Development": SUCCESS,
        "Work": ACCENT_PRIMARY,
    }
    
    def refresh_list():
        timeline_list.controls.clear()
        for i, entry in enumerate(entries):
            week_num = entry.get("week")
            milestone = entry.get("milestone")
            details = entry.get("details", "")
            work_type = entry.get("type", "Work")
            type_color = type_colors.get(work_type, ACCENT_PRIMARY)
            is_first = i == 0
            is_last = i == len(entries) - 1
            
            timeline_list.controls.append(
                Container(
                    content=Row(
                        spacing=20,
                        vertical_alignment="start",
                        controls=[
                            Container(
                                width=80,
                                height=180,
                                content=Column(
                                    spacing=0,
                                    horizontal_alignment="center",
                                    controls=[
                                        Container(width=4, height=24, bgcolor=Colors.TRANSPARENT if is_first else BORDER_COLOR),
                                        Container(
                                            width=60,
                                            height=60,
                                            border_radius=30,
                                            bgcolor=type_color,
                                            border=Border.all(3, BG_MAIN),
                                            content=Column(
                                                alignment="center",
                                                horizontal_alignment="center",
                                                spacing=0,
                                                controls=[
                                                    Text("WEEK", size=9, color=Colors.WHITE, weight="bold"),
                                                    Text(str(week_num), size=22, color=Colors.WHITE, weight="bold"),
                                                ],
                                            ),
                                        ),
                                        Container(width=4, height=100, bgcolor=Colors.TRANSPARENT if is_last else BORDER_COLOR),
                                    ],
                                ),
                            ),
                            Container(
                                expand=True,
                                margin=Padding.only(top=12, bottom=12),
                                padding=24,
                                bgcolor=CARD_BG,
                                border_radius=10,
                                border=Border.all(1, BORDER_COLOR),
                                content=Column(
                                    spacing=14,
                                    controls=[
                                        Row(
                                            alignment="space_between",
                                            vertical_alignment="start",
                                            controls=[
                                                Column(
                                                    expand=True,
                                                    spacing=8,
                                                    controls=[
                                                        Text(milestone, size=17, weight="bold", color=ACCENT_PRIMARY),
                                                        Text(details, size=13, color=TEXT_LIGHT),
                                                    ],
                                                ),
                                                Container(
                                                    padding=Padding.symmetric(vertical=6, horizontal=12),
                                                    border_radius=6,
                                                    bgcolor=type_color,
                                                    content=Text(work_type.upper(), size=10, color=Colors.WHITE, weight="bold"),
                                                ),
                                            ],
                                        ),
                                        Divider(color=BORDER_COLOR, height=1),
                                        Row(
                                            spacing=8,
                                            vertical_alignment="center",
                                            controls=[
                                                Icon(flet.Icons.CHECK_CIRCLE, color=SUCCESS, size=17),
                                                Text("Progress evidence recorded", size=12, color=ACCENT_PRIMARY, weight="bold"),
                                            ],
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                )
            )

    def count_entries(work_type):
        return sum(1 for entry in entries if entry.get("type", "Work") == work_type)

    def metric_card(value, label, color):
        return Container(
            expand=True,
            padding=20,
            border_radius=10,
            bgcolor=CARD_BG,
            border=Border.all(1, BORDER_COLOR),
            content=Column(
                spacing=6,
                controls=[
                    Text(str(value), size=32, weight="bold", color=color),
                    Text(label, size=12, color=TEXT_LIGHT, weight="bold"),
                ],
            ),
        )

    def legend_item(label, color):
        return Row(
            spacing=8,
            vertical_alignment="center",
            controls=[
                Container(width=12, height=12, border_radius=6, bgcolor=color),
                Text(label, size=12, color=TEXT_SECONDARY, weight="bold"),
            ],
        )
    
    refresh_list()
    
    return Container(
        content=Column(
            spacing=0,
            scroll="auto",
            controls=[
                Container(
                    padding=Padding.symmetric(vertical=40, horizontal=48),
                    bgcolor=BG_MAIN,
                    content=Column(
                        spacing=12,
                        controls=[
                            Text("Project Timeline", size=36, weight="bold", color=TEXT_PRIMARY),
                            Text(
                                "A detailed progress map showing how the portfolio evolved from planning through to final polish.",
                                size=15,
                                color=TEXT_SECONDARY,
                            ),
                            Divider(color=ACCENT_SECONDARY, height=2),
                        ],
                    ),
                ),
                Container(
                    padding=Padding.symmetric(vertical=0, horizontal=48),
                    content=Row(
                        spacing=16,
                        controls=[
                            metric_card(len(entries), "Total Milestones", ACCENT_SECONDARY),
                            metric_card(count_entries("Design"), "Design Phases", ACCENT_SECONDARY),
                            metric_card(count_entries("Development"), "Build Phases", SUCCESS),
                            metric_card(count_entries("Branding"), "Brand Phases", ACCENT_CYAN),
                        ],
                    ),
                ),
                Container(
                    padding=Padding.symmetric(vertical=32, horizontal=48),
                    content=Row(
                        alignment="space_between",
                        vertical_alignment="center",
                        controls=[
                            Text("Weekly Progress", size=20, weight="bold", color=TEXT_PRIMARY),
                            Row(
                                spacing=20,
                                controls=[
                                    legend_item("Design", ACCENT_SECONDARY),
                                    legend_item("Branding", ACCENT_CYAN),
                                    legend_item("Development", SUCCESS),
                                ],
                            ),
                        ],
                    ),
                ),
                Container(
                    padding=Padding.only(left=48, right=48, bottom=24),
                    content=timeline_list,
                    expand=True
                ),
                build_footer(),
            ]
        ),
        expand=True,
        bgcolor=BG_MAIN
    )


# ============================================================================
# SECTION 2: GITHUB EVIDENCE
# ============================================================================
def build_github_section(page: Page):
    """Project evidence and design documentation."""
    github_file = os.path.join(os.path.dirname(__file__), "github_evidence.json")
    
    def load_data():
        if os.path.exists(github_file):
            try:
                with open(github_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {"repo": "", "notes": ""}
        return {"repo": "", "notes": ""}
    
    data = load_data()
    github_profile = data.get("repo_url", "https://github.com/NghikomenwaLN")
    repo_value = data.get("repo", "github.com/NghikomenwaLN")
    notes_value = data.get("notes", "")
    impact_value = data.get("impact_summary", "")

    def build_evidence_rows(items, icon_color=SUCCESS):
        rows = []
        for item in items:
            if isinstance(item, dict):
                title = item.get("title", "Contribution evidence")
                details = item.get("details", "")
            else:
                title = str(item)
                details = ""

            rows.append(
                Container(
                    padding=18,
                    border_radius=8,
                    bgcolor=CARD_BG,
                    border=Border.all(1, BORDER_COLOR),
                    content=Row(
                        spacing=12,
                        vertical_alignment=CrossAxisAlignment.START,
                        controls=[
                            Container(
                                width=36,
                                height=36,
                                border_radius=18,
                                bgcolor=icon_color,
                                content=Icon(flet.Icons.CHECK, color=Colors.WHITE, size=18),
                            ),
                            Column(
                                expand=True,
                                spacing=6,
                                controls=[
                                    Text(title, size=14, weight="bold", color=ACCENT_PRIMARY),
                                    Text(details, size=12, color=TEXT_LIGHT),
                                ]
                            )
                        ]
                    )
                )
            )
        return rows

    commit_rows = build_evidence_rows(data.get("commits", []), SUCCESS)
    pr_rows = build_evidence_rows(data.get("pull_requests", []), ACCENT_SECONDARY)

    def evidence_section(title, rows, accent_color):
        return Container(
            expand=True,
            padding=22,
            border_radius=10,
            bgcolor=CARD_BG,
            border=Border.all(1, BORDER_COLOR),
            content=Column(
                spacing=14,
                controls=[
                    Row(
                        spacing=10,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Container(width=5, height=28, border_radius=3, bgcolor=accent_color),
                            Text(title, size=17, weight="bold", color=ACCENT_PRIMARY),
                        ],
                    ),
                    Column(controls=rows, spacing=10),
                ]
            )
        )

    if not commit_rows:
        commit_rows = [
            Container(
                padding=18,
                border_radius=8,
                bgcolor=CARD_BG,
                border=Border.all(1, BORDER_COLOR),
                content=Text("Add commit or design evidence here.", size=13, color=TEXT_LIGHT)
            )
        ]

    if not pr_rows:
        pr_rows = [
            Container(
                padding=18,
                border_radius=8,
                bgcolor=CARD_BG,
                border=Border.all(1, BORDER_COLOR),
                content=Text("Add review or handoff notes here.", size=13, color=TEXT_LIGHT)
            )
        ]

    def summary_tile(label, value, color):
        return Container(
            expand=True,
            padding=20,
            border_radius=10,
            bgcolor=CARD_BG,
            border=Border.all(1, BORDER_COLOR),
            content=Column(
                spacing=6,
                controls=[
                    Text(str(value), size=32, weight="bold", color=color),
                    Text(label, size=12, weight="bold", color=TEXT_LIGHT),
                ],
            ),
        )

    def content_panel(title, body, icon, color):
        return Container(
            expand=True,
            padding=24,
            border_radius=10,
            bgcolor=CARD_BG,
            border=Border.all(1, BORDER_COLOR),
            content=Column(
                spacing=12,
                controls=[
                    Row(
                        spacing=10,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Icon(icon, color=color, size=24),
                            Text(title, size=16, weight="bold", color=ACCENT_PRIMARY),
                        ],
                    ),
                    Text(body or "Add a short summary here.", size=13, color=TEXT_LIGHT),
                ],
            ),
        )
    
    return Container(
        content=Column(
            spacing=0,
            scroll="auto",
            controls=[
                Container(
                    padding=Padding.symmetric(vertical=40, horizontal=48),
                    bgcolor=BG_MAIN,
                    content=Column(
                        spacing=12,
                        controls=[
                            Text("GitHub Evidence", size=36, weight="bold", color=TEXT_PRIMARY),
                            Text(
                                "Repository details, contribution evidence, and design documentation.",
                                size=15,
                                color=TEXT_SECONDARY,
                            ),
                            Divider(color=ACCENT_SECONDARY, height=2),
                        ]
                    ),
                ),
                Container(
                    padding=Padding.symmetric(vertical=0, horizontal=48),
                    content=Column(
                        spacing=20,
                        controls=[
                            Container(
                                padding=24,
                                border_radius=10,
                                bgcolor=CARD_BG,
                                border=Border.all(1, BORDER_COLOR),
                                content=Row(
                                    spacing=18,
                                    vertical_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Container(
                                            width=56,
                                            height=56,
                                            border_radius=10,
                                            bgcolor=ACCENT_SECONDARY,
                                            content=Icon(flet.Icons.CODE, color=Colors.WHITE, size=32),
                                        ),
                                        Column(
                                            expand=True,
                                            spacing=4,
                                            controls=[
                                                Text("Repository", size=12, weight="bold", color=TEXT_LIGHT),
                                                Text(repo_value, size=18, weight="bold", color=ACCENT_PRIMARY),
                                            ],
                                        ),
                                        Button(
                                            "Open GitHub",
                                            icon=flet.Icons.OPEN_IN_NEW,
                                            url=github_profile,
                                            bgcolor=ACCENT_SECONDARY,
                                            color=Colors.WHITE,
                                            height=44,
                                        ),
                                    ],
                                ),
                            ),
                            Row(
                                spacing=14,
                                controls=[
                                    summary_tile("Evidence Items", len(commit_rows), SUCCESS),
                                    summary_tile("Review Notes", len(pr_rows), ACCENT_SECONDARY),
                                    summary_tile("Primary Role", "Firebase", ACCENT_SECONDARY),
                                ],
                            ),
                            Row(
                                spacing=14,
                                vertical_alignment=CrossAxisAlignment.START,
                                controls=[
                                    content_panel("Role Summary", notes_value, flet.Icons.DESIGN_SERVICES, ACCENT_SECONDARY),
                                    content_panel("Impact Summary", impact_value, flet.Icons.INSIGHTS, SUCCESS),
                                ],
                            ),
                            Row(
                                spacing=14,
                                vertical_alignment=CrossAxisAlignment.START,
                                controls=[
                                    evidence_section("Design Evidence", commit_rows, SUCCESS),
                                    evidence_section("Review & Handoff", pr_rows, ACCENT_SECONDARY),
                                ],
                            ),
                        ]
                    ),
                    expand=True
                ),
                build_footer(),
            ]
        ),
        expand=True,
        bgcolor=BG_MAIN
    )


# ============================================================================
# SECTION 3: TECHNICAL BLOG
# ============================================================================
def build_blog_section():
    """Reflection journal with video playback."""
    
    blog_file = os.path.join(os.path.dirname(__file__), "blog_posts.json")
    
    def load_posts():
        if os.path.exists(blog_file):
            try:
                with open(blog_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []
    
    posts = load_posts()
    posts_list = Column(spacing=24, scroll="auto")
    
    def refresh_posts():
        posts_list.controls.clear()
        if not posts:
            posts_list.controls.append(
                Container(
                    padding=32,
                    content=Text(
                        "No reflection entries have been added yet.",
                        size=15, color=TEXT_SECONDARY, italic=True
                    )
                )
            )
        else:
            for post in posts:
                title = post.get("title", "Project Reflection")
                video_file = post.get("video_file", "")
                description = post.get("description", "")
                
                card_controls = [
                    Text(title, size=22, weight="bold", color=ACCENT_PRIMARY),
                ]
                
                if description:
                    card_controls.append(
                        Text(description, size=14, color=TEXT_LIGHT, italic=True)
                    )
                
                if video_file:
                    video_path = os.path.join(os.path.dirname(__file__), "assets", video_file)
                    
                    if os.path.exists(video_path):
                        video_resource = video_file.replace(os.sep, "/")
                        card_controls.append(
                            Container(
                                height=480,
                                border_radius=12,
                                clip_behavior=ClipBehavior.HARD_EDGE,
                                bgcolor=Colors.BLACK,
                                border=Border.all(2, ACCENT_SECONDARY),
                                content=Video(
                                    playlist=[VideoMedia(video_resource)],
                                    title=title,
                                    fit=flet.BoxFit.CONTAIN,
                                    fill_color=Colors.BLACK,
                                    autoplay=False,
                                    muted=False,
                                    wakelock=True,
                                    expand=True,
                                )
                            )
                        )
                    else:
                        card_controls.append(
                            Container(
                                height=220,
                                border_radius=12,
                                bgcolor=CARD_BG,
                                border=Border.all(2, BORDER_COLOR),
                                padding=24,
                                content=Column(
                                    alignment="center",
                                    horizontal_alignment="center",
                                    spacing=8,
                                    controls=[
                                        Icon(flet.Icons.VIDEO_FILE, size=48, color=TEXT_SECONDARY),
                                        Text(
                                            "Video Not Found",
                                            size=14,
                                            weight="bold",
                                            color=ACCENT_PRIMARY
                                        ),
                                        Text(
                                            f"File: {video_file}",
                                            size=12,
                                            color=TEXT_SECONDARY
                                        ),
                                    ]
                                )
                            )
                        )
                else:
                    card_controls.append(
                        Container(
                            height=220,
                            border_radius=12,
                            bgcolor=CARD_BG,
                            border=Border.all(2, BORDER_COLOR),
                            padding=24,
                            content=Column(
                                alignment="center",
                                horizontal_alignment="center",
                                spacing=8,
                                controls=[
                                    Icon(flet.Icons.VIDEO_LIBRARY, size=48, color=TEXT_SECONDARY),
                                    Text(
                                        "Video Coming Soon",
                                        size=14,
                                        weight="bold",
                                        color=ACCENT_PRIMARY
                                    ),
                                    Text(
                                        "A project reflection video will appear here",
                                        size=12,
                                        color=TEXT_LIGHT
                                    ),
                                ]
                            )
                        )
                    )
                
                posts_list.controls.append(
                    Container(
                        padding=24,
                        border_radius=12,
                        bgcolor=CARD_BG,
                        border=Border.all(1, BORDER_COLOR),
                        content=Column(
                            spacing=18,
                            controls=card_controls
                        )
                    )
                )
    
    refresh_posts()
    
    return Container(
        content=Column(
            spacing=0,
            scroll="auto",
            controls=[
                Container(
                    padding=Padding.symmetric(vertical=40, horizontal=48),
                    bgcolor=BG_MAIN,
                    content=Column(
                        spacing=12,
                        controls=[
                            Text("Reflection Journal", size=36, weight="bold", color=TEXT_PRIMARY),
                            Text("Project insights, learning notes, and video evidence",
                                 size=15, color=TEXT_SECONDARY),
                            Divider(color=ACCENT_SECONDARY, height=2),
                        ]
                    )
                ),
                Container(
                    padding=Padding.symmetric(vertical=0, horizontal=48),
                    content=posts_list,
                    expand=True,
                ),
                build_footer(),
            ]
        ),
        expand=True,
        bgcolor=BG_MAIN
    )


# ============================================================================
# SECTION 4: MATLAB CERTIFICATES
# ============================================================================
def build_matlab_section():
    """MATLAB certificate gallery."""
    certificates = [
        ("MATLAB Onramp", "matlab_certificate_1.jpg", "certificate (1).pdf"),
        ("Data Visualization", "matlab_certificate_2.jpg", "certificate (2).pdf"),
        ("Make and Manipulate Matrices", "matlab_certificate_3.jpg", "certificate (3).pdf"),
        ("Optimization Onramp", "matlab_certificate_4.jpg", "certificate (4).pdf"),
        ("Statistics Onramp", "matlab_certificate_5.jpg", "certificate (5).pdf"),
        ("Explore Data with MATLAB Plots", "matlab_certificate_6.jpg", "certificate (6).pdf"),
    ]

    certificate_cards = []
    for title, image_file, pdf_file in certificates:
        certificate_cards.append(
            Container(
                width=540,
                padding=16,
                border_radius=10,
                bgcolor=CARD_BG,
                border=Border.all(1, BORDER_COLOR),
                content=Column(
                    spacing=14,
                    controls=[
                        Container(
                            height=340,
                            border_radius=8,
                            clip_behavior=ClipBehavior.ANTI_ALIAS,
                            bgcolor=BG_SECONDARY,
                            content=Image(
                                src=image_file,
                                fit="contain",
                                expand=True,
                            ),
                        ),
                        Row(
                            spacing=12,
                            vertical_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                Text(
                                    title,
                                    size=14,
                                    weight="bold",
                                    color=ACCENT_PRIMARY,
                                    expand=True,
                                ),
                                Button(
                                    "View PDF",
                                    icon=flet.Icons.OPEN_IN_NEW,
                                    width=130,
                                    height=40,
                                    bgcolor=ACCENT_SECONDARY,
                                    color=Colors.WHITE,
                                    url=pdf_file,
                                ),
                            ],
                        ),
                    ],
                ),
            )
        )

    certificate_rows = [
        Row(
            spacing=20,
            vertical_alignment=CrossAxisAlignment.START,
            controls=certificate_cards[index:index + 2],
        )
        for index in range(0, len(certificate_cards), 2)
    ]
    
    return Container(
        content=Column(
            spacing=0,
            scroll="auto",
            controls=[
                Container(
                    padding=Padding.symmetric(vertical=40, horizontal=48),
                    bgcolor=BG_MAIN,
                    content=Column(
                        spacing=12,
                        controls=[
                            Text("MATLAB Certificates", size=36, weight="bold", color=TEXT_PRIMARY),
                            Text(f"{len(certificates)} professional learning certifications",
                                 size=15, color=TEXT_SECONDARY),
                            Divider(color=ACCENT_SECONDARY, height=2),
                        ]
                    )
                ),
                Container(
                    padding=Padding.symmetric(vertical=0, horizontal=48),
                    content=Column(
                        spacing=20,
                        controls=certificate_rows,
                    ),
                    expand=True
                ),
                build_footer(),
            ]
        ),
        expand=True,
        bgcolor=BG_MAIN
    )


# ============================================================================
# MAIN APP
# ============================================================================
def main(page: Page):
    """Main application function"""
    suppress_windows_connection_reset_noise()
    page.title = "Gerhard Mangundu | Project Portfolio"
    page.window_width = 1200
    page.window_height = 900
    page.scroll = "auto"
    page.bgcolor = BG_MAIN
    
    pages_container = Container(expand=True)
    current_page_index = 0
    nav_buttons = Row(spacing=8)

    nav_items = [
        ("Home", flet.Icons.HOME, 0),
        ("Timeline", flet.Icons.TIMELINE, 1),
        ("GitHub", flet.Icons.CODE, 2),
        ("Blog", flet.Icons.ARTICLE, 3),
        ("MATLAB", flet.Icons.SCHOOL, 4),
    ]

    def build_nav_button(label, icon, index):
        is_active = current_page_index == index
        return Button(
            label,
            icon=icon,
            height=46,
            width=150,
            bgcolor=ACCENT_SECONDARY if is_active else Colors.TRANSPARENT,
            color=Colors.WHITE if is_active else TEXT_SECONDARY,
            style=ButtonStyle(text_style=TextStyle(size=13, weight="bold")),
            on_click=lambda e, selected=index: navigate_to(selected),
        )

    def refresh_nav():
        nav_buttons.controls = [
            build_nav_button(label, icon, index)
            for label, icon, index in nav_items
        ]
    
    def navigate_to(index):
        nonlocal current_page_index
        current_page_index = index
        if index == 0:
            pages_container.content = build_landing_page(navigate_to)
        elif index == 1:
            pages_container.content = build_timeline_section()
        elif index == 2:
            pages_container.content = build_github_section(page)
        elif index == 3:
            pages_container.content = build_blog_section()
        elif index == 4:
            pages_container.content = build_matlab_section()
        refresh_nav()
        page.update()
    
    nav_bar = Container(
        padding=Padding.symmetric(vertical=14, horizontal=20),
        bgcolor=ACCENT_PRIMARY,
        border=Border(bottom=border_radius.BorderSide(1, Colors.WHITE10)),
        content=Row(
            alignment="space_between",
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Column(
                    spacing=2,
                    controls=[
                        Text("Gerhard Mangundu", size=17, weight="bold", color=Colors.WHITE),
                        Text("Portfolio — Firebase Lead", size=11, color=TEXT_SECONDARY),
                    ],
                ),
                nav_buttons,
            ],
        ),
    )
    
    page.add(
        nav_bar,
        pages_container
    )
    
    navigate_to(0)


if __name__ == "__main__":
    run_portfolio_app()
