import type { ClineMessage, ExtensionMessage } from "@roo-code/types"

import { MessageProcessor } from "../message-processor.js"
import { StateStore } from "../state-store.js"
import { TypedEventEmitter, type TaskCompletedEvent } from "../events.js"

function createMessage(overrides: Partial<ClineMessage>): ClineMessage {
	return { ts: Date.now() + Math.random() * 1000, type: "say", ...overrides }
}

function createStateMessage(messages: ClineMessage[]): ExtensionMessage {
	return { type: "state", state: { clineMessages: messages } } as ExtensionMessage
}

describe("MessageProcessor taskCompleted semantics", () => {
	it("emits successful completion only for completion_result", () => {
		const store = new StateStore()
		const emitter = new TypedEventEmitter()
		const processor = new MessageProcessor(store, emitter)

		const events: TaskCompletedEvent[] = []
		emitter.on("taskCompleted", (event) => events.push(event))

		processor.processMessage(createStateMessage([createMessage({ type: "say", say: "text", text: "working" })]))
		processor.processMessage(
			createStateMessage([createMessage({ type: "ask", ask: "completion_result", partial: false })]),
		)

		expect(events).toHaveLength(1)
		expect(events[0]?.success).toBe(true)
	})

	it("emits non-success completion for resume_completed_task transition", () => {
		const store = new StateStore()
		const emitter = new TypedEventEmitter()
		const processor = new MessageProcessor(store, emitter)

		const events: TaskCompletedEvent[] = []
		emitter.on("taskCompleted", (event) => events.push(event))

		processor.processMessage(createStateMessage([createMessage({ type: "say", say: "text", text: "working" })]))
		processor.processMessage(
			createStateMessage([createMessage({ type: "ask", ask: "resume_completed_task", partial: false })]),
		)

		expect(events).toHaveLength(1)
		expect(events[0]?.success).toBe(false)
	})
})
