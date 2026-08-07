import asyncio
from argparse import ArgumentParser
from typing import Any
from utils.reflection import get_class_fqcn
from utils.context import Context
from utils.base_handler import BaseHandler


def parse_args() -> dict[str, Any]:
    parser = ArgumentParser()
    parser.add_argument("--handler_fqcn", type=str, help="fqcn of the handler")
    parsed_args = parser.parse_args()
    return vars(parsed_args)


async def handle(handler_fqcn: str) -> None:
    context = Context.bootstrap()
    handler_cls = get_class_fqcn(handler_fqcn, as_instance=False)

    if not issubclass(handler_cls, BaseHandler):
        raise TypeError(f"{handler_cls} is not a BaseHandler")

    handler = handler_cls(context=context)
    return await handler.run_handler()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(handle(**args))
