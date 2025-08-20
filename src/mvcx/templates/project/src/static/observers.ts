type Handler = (data: any) => void;

type Subjects = Record<string, Handler[]>;

class Observer {
  private _subjects: Subjects;

  constructor(subjects: Subjects) {
    this._subjects = subjects;
  }

  attach(event: string, handler: Handler): void {
    this._subjects[event]?.push(handler);
  }

  detach(event: string, handler: Handler): void {
    let handlers = this._subjects[event]!;
    handlers = handlers.filter((value) => value !== handler);
    this._subjects[event] = handlers;
  }

  notify(event: string, data: any): void {
    this._subjects[event]?.forEach((handler) => {
      handler(data);
    });
  }
}

export const appObserver = new Observer({
  "theme-change": [],
});
