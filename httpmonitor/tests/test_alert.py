import os
import pytest
import asyncio
from httpmonitor.monitor import alert_handler

@pytest.mark.asyncio
async def test_alert_creates(event_loop):
    alert_queue = asyncio.Queue(loop=event_loop)
    alert_queue_msg = asyncio.Queue(loop=event_loop)

    # Call the alert_handler with 10 items in the queue and threshold of 9 so it creates an alert message
    for i in range(10):
        await alert_queue.put(i)
    await alert_handler(alert_queue, alert_queue_msg, threshold=9, stop=True)

    # Check alert
    message = await alert_queue_msg.get()
    assert len(message) is not None
    assert message["type"] == "alert"
    assert message["hits"] == 10

    # Now we call the alert_handler again, simulating that the time passed
    # since the queue is empty it should a new recover message
    await alert_handler(alert_queue, alert_queue_msg, current_alert=True, stop=True)
    message = await alert_queue_msg.get()
    assert len(message) is not None
    assert message["type"] == "recover"
    assert message["hits"] == 0
