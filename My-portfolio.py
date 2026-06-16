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
# FORMAL COLOR SCHEME - graphite, steel blue, ivory, and restrained amber
# ============================================================================
BG_MAIN = "#0F1720"
BG_SECONDARY = "#E8EDF2"
ACCENT_PRIMARY = "#263746"
ACCENT_SECONDARY = "#C69A45"
SUCCESS = "#2F6F5E"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#D7DEE8"
TEXT_LIGHT = "#5F6F82"
CARD_BG = "#F7F9FC"
BORDER_COLOR = "#BFC9D5"
ACCENT_CYAN = "#52738A"
FOOTER_BG = "#08111C"

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
            spacing=22,
            scroll="auto",
            controls=[
                Container(
                    padding=Padding.symmetric(vertical=36, horizontal=36),
                    bgcolor=ACCENT_PRIMARY,
                    content=Row(
                        alignment="space_between",
                        vertical_alignment="center",
                        spacing=28,
                        controls=[
                            Column(
                                expand=True,
                                spacing=18,
                                controls=[
                                    Text("Gerhard Mangundu", size=40, weight="bold", color=Colors.WHITE),
                                    Text(
                                        "Firebase Lead - Group 10 - Blast Master Pro",
                                        size=18,
                                        color=TEXT_SECONDARY,
                                    ),
                                    Text(
                                        "This portfolio presents my Mining project contribution for Blast Master Pro. My main responsibility was "
                                        "leading the Firebase work: setting up cloud services, supporting authentication, managing data flow, "
                                        "and helping the app connect reliably to the backend.",
                                        size=15,
                                        color=TEXT_SECONDARY,
                                    ),
                                    Button(
                                        "View Timeline",
                                        width=210,
                                        height=48,
                                        bgcolor=ACCENT_SECONDARY,
                                        color=Colors.WHITE,
                                        style=ButtonStyle(text_style=TextStyle(size=16)),
                                        on_click=lambda e: on_nav(1),
                                    ),
                                ],
                            ),
                            Container(
                                width=330,
                                height=330,
                                border_radius=4,
                                bgcolor=BG_SECONDARY,
                                border=Border.all(2, ACCENT_SECONDARY),
                                clip_behavior=ClipBehavior.HARD_EDGE,
                                content=Image(src=image_src or "", fit="cover", expand=True),
                            ),
                        ],
                    ),
                ),
                Container(
                    padding=Padding.symmetric(vertical=0, horizontal=32),
                    content=Row(
                        spacing=14,
                        controls=[
                            Container(
                                expand=True,
                                padding=18,
                                border_radius=4,
                                bgcolor=Colors.WHITE,
                                border=Border.all(1, BORDER_COLOR),
                                content=Column(
                                    spacing=6,
                                    controls=[
                                        Text(number, size=28, weight="bold", color=ACCENT_SECONDARY if number != "04" else SUCCESS),
                                        Text(title, size=15, color=ACCENT_PRIMARY, weight="bold"),
                                        Text(body, size=12, color=TEXT_LIGHT),
                                    ],
                                ),
                            )
                            for number, title, body in highlights
                        ],
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
        padding=25,
        content=Column(
            spacing=12,
            controls=[
                Divider(color=Colors.WHITE10, height=1),
                Row(
                    alignment="space_between",
                    controls=[
                        Column(
                            spacing=8,
                            controls=[
                                Text("Gerhard Mangundu Portfolio", size=12, weight="bold", color=Colors.WHITE),
                                Text("Mining App Development and Firebase Leadership", size=11, color=Colors.WHITE60),
                            ]
                        ),
                        Column(
                            spacing=8,
                            horizontal_alignment="end",
                            controls=[
                                Text(f"© {datetime.now().year} Gerhard Mangundu. All rights reserved.", 
                                     size=11, color=Colors.WHITE60),
                                Text("Group 10 - Blast Master Pro", size=11, color=ACCENT_CYAN),
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
            spacing=4,
            controls=[
                Icon(flet.Icons.CHECK_CIRCLE, color=SUCCESS, size=18),
                Text("Complete", size=12, color=SUCCESS, weight="bold")
            ]
        )
    else:
        status_text = label or "View Details"
        return Row(
            spacing=4,
            controls=[
                Icon(flet.Icons.INFO, color=ACCENT_PRIMARY, size=18),
                Text(status_text, size=12, color=ACCENT_PRIMARY, weight="bold")
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
                        spacing=18,
                        vertical_alignment="start",
                        controls=[
                            Container(
                                width=78,
                                height=176,
                                content=Column(
                                    spacing=0,
                                    horizontal_alignment="center",
                                    controls=[
                                        Container(width=4, height=24, bgcolor=Colors.TRANSPARENT if is_first else BORDER_COLOR),
                                        Container(
                                            width=56,
                                            height=56,
                                            border_radius=28,
                                            bgcolor=type_color,
                                            border=Border.all(4, BG_SECONDARY),
                                            content=Column(
                                                alignment="center",
                                                horizontal_alignment="center",
                                                spacing=0,
                                                controls=[
                                                    Text("WEEK", size=9, color=Colors.WHITE, weight="bold"),
                                                    Text(str(week_num), size=21, color=Colors.WHITE, weight="bold"),
                                                ],
                                            ),
                                        ),
                                        Container(width=4, height=96, bgcolor=Colors.TRANSPARENT if is_last else BORDER_COLOR),
                                    ],
                                ),
                            ),
                            Container(
                                expand=True,
                                margin=Padding.only(top=12, bottom=12),
                                padding=22,
                                bgcolor=CARD_BG,
                                border_radius=8,
                                border=Border.all(1, BORDER_COLOR),
                                content=Column(
                                    spacing=12,
                                    controls=[
                                        Row(
                                            alignment="space_between",
                                            vertical_alignment="start",
                                            controls=[
                                                Column(
                                                    expand=True,
                                                    spacing=6,
                                                    controls=[
                                                        Text(milestone, size=17, weight="bold", color=ACCENT_PRIMARY),
                                                        Text(details, size=13, color=TEXT_LIGHT),
                                                    ],
                                                ),
                                                Container(
                                                    padding=Padding.symmetric(vertical=6, horizontal=10),
                                                    border_radius=4,
                                                    bgcolor=type_color,
                                                    content=Text(work_type.upper(), size=10, color=Colors.WHITE, weight="bold"),
                                                ),
                                            ],
                                        ),
                                        Container(height=1, bgcolor=BG_SECONDARY),
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
            padding=18,
            border_radius=8,
            bgcolor=CARD_BG,
            border=Border.all(1, BORDER_COLOR),
            content=Column(
                spacing=4,
                controls=[
                    Text(str(value), size=28, weight="bold", color=color),
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
            spacing=22,
            scroll="auto",
            controls=[
                Container(
                    padding=Padding.symmetric(vertical=30, horizontal=32),
                    bgcolor=ACCENT_PRIMARY,
                    content=Row(
                        alignment="space_between",
                        vertical_alignment="center",
                        spacing=24,
                        controls=[
                            Column(
                                expand=True,
                                spacing=8,
                                controls=[
                                    Text("Project Timeline", size=34, weight="bold", color=TEXT_PRIMARY),
                                    Text(
                                        "A cleaner progress map showing how the portfolio moved from planning to interface build and polish.",
                                        size=14,
                                        color=TEXT_SECONDARY,
                                    ),
                                ],
                            ),
                            Container(
                                padding=Padding.symmetric(vertical=10, horizontal=14),
                                border_radius=8,
                                bgcolor=Colors.WHITE10,
                                border=Border.all(1, Colors.WHITE24),
                                content=Text(f"{len(entries)} recorded weeks", size=13, color=Colors.WHITE, weight="bold"),
                            ),
                        ],
                    ),
                ),
                Container(
                    padding=Padding.symmetric(vertical=0, horizontal=32),
                    content=Row(
                        spacing=14,
                        controls=[
                            metric_card(len(entries), "Total milestones", ACCENT_PRIMARY),
                            metric_card(count_entries("Design"), "Design phases", ACCENT_SECONDARY),
                            metric_card(count_entries("Development"), "Build phases", SUCCESS),
                            metric_card(count_entries("Branding"), "Brand phase", ACCENT_CYAN),
                        ],
                    ),
                ),
                Container(
                    padding=Padding.symmetric(vertical=0, horizontal=32),
                    content=Row(
                        alignment="space_between",
                        vertical_alignment="center",
                        controls=[
                            Text("Weekly Progress", size=20, weight="bold", color=TEXT_PRIMARY),
                            Row(
                                spacing=18,
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
                    padding=Padding.only(left=32, right=32, bottom=24),
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
                    padding=16,
                    border_radius=8,
                    bgcolor=CARD_BG,
                    border=Border.all(1, BORDER_COLOR),
                    content=Row(
                        spacing=12,
                        vertical_alignment=CrossAxisAlignment.START,
                        controls=[
                            Container(
                                width=34,
                                height=34,
                                border_radius=17,
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
            padding=20,
            border_radius=8,
            bgcolor=BG_SECONDARY,
            border=Border.all(1, BORDER_COLOR),
            content=Column(
                spacing=14,
                controls=[
                    Row(
                        spacing=10,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Container(width=5, height=26, border_radius=3, bgcolor=accent_color),
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
            padding=18,
            border_radius=8,
            bgcolor=CARD_BG,
            border=Border.all(1, BORDER_COLOR),
            content=Column(
                spacing=4,
                controls=[
                    Text(str(value), size=28, weight="bold", color=color),
                    Text(label, size=12, weight="bold", color=TEXT_LIGHT),
                ],
            ),
        )

    def content_panel(title, body, icon, color):
        return Container(
            expand=True,
            padding=22,
            border_radius=8,
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
                            Text(title, size=17, weight="bold", color=ACCENT_PRIMARY),
                        ],
                    ),
                    Text(body or "Add a short summary here.", size=13, color=TEXT_LIGHT),
                ],
            ),
        )
    
    return Container(
        content=Column(
            spacing=22,
            scroll="auto",
            controls=[
                Container(
                    padding=Padding.symmetric(vertical=30, horizontal=32),
                    bgcolor=ACCENT_PRIMARY,
                    content=Row(
                        alignment="space_between",
                        vertical_alignment="center",
                        spacing=24,
                        controls=[
                            Column(
                                expand=True,
                                spacing=8,
                                controls=[
                                    Text("GitHub Evidence", size=34, weight="bold", color=TEXT_PRIMARY),
                                    Text(
                                        "Repository, design role, contribution evidence, and review notes for the BlastX project.",
                                        size=14,
                                        color=TEXT_SECONDARY,
                                    ),
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
                Container(
                    padding=Padding.symmetric(vertical=0, horizontal=32),
                    content=Column(
                        spacing=18,
                        controls=[
                            Container(
                                padding=22,
                                border_radius=8,
                                bgcolor=BG_SECONDARY,
                                border=Border.all(1, BORDER_COLOR),
                                content=Row(
                                    spacing=16,
                                    vertical_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Container(
                                            width=52,
                                            height=52,
                                            border_radius=8,
                                            bgcolor=ACCENT_PRIMARY,
                                            content=Icon(flet.Icons.CODE, color=Colors.WHITE, size=28),
                                        ),
                                        Column(
                                            expand=True,
                                            spacing=4,
                                            controls=[
                                                Text("Repository", size=12, weight="bold", color=TEXT_LIGHT),
                                                Text(repo_value, size=18, weight="bold", color=ACCENT_PRIMARY),
                                            ],
                                        ),
                                        Container(
                                            padding=Padding.symmetric(vertical=8, horizontal=12),
                                            border_radius=4,
                                            bgcolor=ACCENT_PRIMARY,
                                            content=Text("UI/UX Design Contribution", size=12, color=Colors.WHITE, weight="bold"),
                                        ),
                                    ],
                                ),
                            ),
                            Row(
                                spacing=14,
                                controls=[
                                    summary_tile("Evidence items", len(commit_rows), SUCCESS),
                                    summary_tile("Review notes", len(pr_rows), ACCENT_SECONDARY),
                                    summary_tile("Primary role", "UI/UX", ACCENT_PRIMARY),
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
    posts_list = Column(spacing=20, scroll="auto")
    
    def refresh_posts():
        posts_list.controls.clear()
        if not posts:
            posts_list.controls.append(
                Container(
                    padding=20,
                    content=Text(
                        "No reflection entries have been added yet.",
                        size=14, color=TEXT_SECONDARY, italic=True
                    )
                )
            )
        else:
            for post in posts:
                title = post.get("title", "Project Reflection")
                video_file = post.get("video_file", "")
                description = post.get("description", "")
                
                card_controls = [
                    Container(
                        padding=Padding.symmetric(vertical=0, horizontal=10),
                        content=Text(title, size=22, weight="bold", color=TEXT_PRIMARY)
                    ),
                ]
                
                if description:
                    card_controls.append(
                        Container(
                            padding=Padding.symmetric(vertical=0, horizontal=10),
                            content=Text(description, size=14, color=TEXT_SECONDARY, italic=True)
                        )
                    )
                
                if video_file:
                    video_path = os.path.join(os.path.dirname(__file__), "assets", video_file)
                    
                    if os.path.exists(video_path):
                        video_resource = video_file.replace(os.sep, "/")
                        card_controls.append(
                            Container(
                                height=460,
                                border_radius=15,
                                clip_behavior=ClipBehavior.HARD_EDGE,
                                bgcolor=Colors.BLACK,
                                border=Border.all(3, ACCENT_SECONDARY),
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
                                height=200,
                                border_radius=10,
                                bgcolor=BG_SECONDARY,
                                border=Border.all(2, BORDER_COLOR),
                                padding=20,
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
                                            color=TEXT_PRIMARY
                                        ),
                                        Text(
                                            f"File: {video_file}",
                                            size=12,
                                            color=TEXT_SECONDARY
                                        ),
                                        Text(
                                            f"Place video in: assets/{video_file}",
                                            size=11,
                                            color=TEXT_LIGHT
                                        ),
                                    ]
                                )
                            )
                        )
                else:
                    card_controls.append(
                        Container(
                            height=200,
                            border_radius=10,
                            bgcolor=BG_SECONDARY,
                            border=Border.all(2, BORDER_COLOR),
                            padding=20,
                            content=Column(
                                alignment="center",
                                horizontal_alignment="center",
                                spacing=8,
                                controls=[
                                    Icon(flet.Icons.VIDEO_LIBRARY, size=48, color=TEXT_SECONDARY),
                                    Text(
                                        "Video Will Be Added",
                                        size=14,
                                        weight="bold",
                                        color=TEXT_PRIMARY
                                    ),
                                    Text(
                                        "A short project reflection video will appear here",
                                        size=12,
                                        color=TEXT_SECONDARY
                                    ),
                                ]
                            )
                        )
                    )
                
                posts_list.controls.append(
                    Card(
                        elevation=4,
                        content=Container(
                            padding=20,
                            bgcolor=ACCENT_PRIMARY,
                            border_radius=8,
                            content=Column(
                                spacing=20,
                                controls=card_controls
                            )
                        )
                    )
                )
    
    refresh_posts()
    
    return Container(
        content=Column(
            spacing=20,
            scroll="auto",
            controls=[
                Container(
                    padding=Padding.symmetric(vertical=30, horizontal=32),
                    bgcolor=ACCENT_PRIMARY,
                    content=Column(
                        spacing=8,
                        controls=[
                            Text("Reflection Journal", size=32, weight="bold", color=TEXT_PRIMARY),
                            Text("Short notes and video evidence from the project process",
                                 size=16, color=TEXT_SECONDARY),
                            Container(
                                width=100,
                                content=Divider(color=ACCENT_SECONDARY, thickness=2),
                            ),
                        ]
                    )
                ),
                Container(
                    padding=Padding.symmetric(vertical=0, horizontal=32),
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
                width=520,
                padding=14,
                border_radius=4,
                bgcolor=CARD_BG,
                border=Border.all(1, BORDER_COLOR),
                content=Column(
                    spacing=12,
                    controls=[
                        Container(
                            height=320,
                            border_radius=3,
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
                                    "Open PDF",
                                    icon=flet.Icons.OPEN_IN_NEW,
                                    width=130,
                                    height=38,
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
            spacing=18,
            vertical_alignment=CrossAxisAlignment.START,
            controls=certificate_cards[index:index + 2],
        )
        for index in range(0, len(certificate_cards), 2)
    ]
    
    return Container(
        content=Column(
            spacing=20,
            scroll="auto",
            controls=[
                Container(
                    padding=Padding.symmetric(vertical=30, horizontal=32),
                    bgcolor=ACCENT_PRIMARY,
                    content=Column(
                        spacing=8,
                        controls=[
                            Text("MATLAB Certificates", size=28, weight="bold", color=TEXT_PRIMARY),
                            Text(f"{len(certificates)} MathWorks learning certificates",
                                 size=14, color=TEXT_SECONDARY),
                        ]
                    )
                ),
                Container(
                    padding=Padding.symmetric(vertical=0, horizontal=32),
                    content=Column(
                        spacing=18,
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
            height=44,
            width=142,
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
        padding=Padding.symmetric(vertical=12, horizontal=18),
        bgcolor=ACCENT_PRIMARY,
        border=Border.all(1, Colors.WHITE24),
        content=Row(
            alignment="space_between",
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Column(
                    spacing=2,
                    controls=[
                        Text("Gerhard Portfolio", size=16, weight="bold", color=Colors.WHITE),
                        Text("Project showcase", size=11, color=TEXT_SECONDARY),
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
