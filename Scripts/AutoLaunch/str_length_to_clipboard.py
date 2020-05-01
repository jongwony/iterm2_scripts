import asyncio

import Foundation
import AppKit
import iterm2


def to_html(text):
    return f"<pre>{text}</pre>"


async def save_clipboard(text):
    """
    Referer :: pyperclip sources
    """
    new_str = Foundation.NSString.stringWithString_(str(text)).nsstring()
    new_data = new_str.dataUsingEncoding_(Foundation.NSUTF8StringEncoding)
    board = AppKit.NSPasteboard.generalPasteboard()
    board.declareTypes_owner_([AppKit.NSStringPboardType], None)
    board.setData_forType_(new_data, AppKit.NSStringPboardType)
    await asyncio.sleep(0)


async def main(connection):
    app = await iterm2.async_get_app(connection)

    # Set the click handler
    @iterm2.RPC
    async def onclick(session_id):
        session = app.get_session_by_id(session_id)
        selection = await session.async_get_selection()
        selected_text = await session.async_get_selection_text(selection)
        length = str(len(selected_text.strip()))
        await save_clipboard(length)
        await component.async_open_popover(session_id, to_html(f'{length} Copied!'), iterm2.util.Size(100, 50))

    # Define the configuration knobs:
    vl = "calculate_selected_length"
    knobs = [iterm2.CheckboxKnob("Calculate Selected Length", False, vl)]
    component = iterm2.StatusBarComponent(
        short_description="Calculate Selected Length",
        detailed_description="Select string in the terminal, then click this status bar component to see it length.",
        knobs=knobs,
        exemplar="len(selected)",
        update_cadence=None,
        identifier="com.iterm2.calculate-selected-length")

    # This function gets called whenever any of the paths named in defaults (below) changes
    # or its configuration changes.
    @iterm2.StatusBarRPC
    async def coro(knobs):
        return ["len(selected)"]

    # Register the component.
    await component.async_register(connection, coro, onclick=onclick)


iterm2.run_forever(main)
