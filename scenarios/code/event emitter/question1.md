# Typed Event Emitter

Implement a generic TypeScript class called `TypedEventEmitter`.

## Requirements
- The class should be generic over an event map, for example:
  ```ts
  type Events = {
    data: { value: number };
    error: { message: string };
    done: void;
  };
  ```
- Provide these methods:
  - `on<K extends keyof Events>(event: K, listener: (payload: Events[K]) => void): void`
  - `off<K extends keyof Events>(event: K, listener: (payload: Events[K]) => void): void`
  - `once<K extends keyof Events>(event: K, listener: (payload: Events[K]) => void): void`
  - `emit<K extends keyof Events>(event: K, payload: Events[K]): void`
- `once` must call the listener only the first time the event is emitted, then remove it.
- `off` must remove only the exact listener function that was passed.
- Emitting an event with no listeners should do nothing.
- The same listener can be registered more than once; each registration is independent.
- Do not use any external libraries.
- Include a few lines of example usage at the bottom that show `on`, `once`, `emit`, and `off` working with the sample event map above.

## Deliverables
Produce one complete TypeScript file (for example `TypedEventEmitter.ts`) that contains the class and the example usage.
