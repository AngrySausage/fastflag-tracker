from modules import request
from modules.request import Response, API


def get_fastflags() -> dict:
    response: Response = request.get(API.FASTFLAGS)
    data: dict = response.json()
    fastflags: dict = data["applicationSettings"]

    # Filter out fastflags with given suffix or specific flags
    filter: list[str] = [
        flag for flag in fastflags
        if isinstance(flag, str) and (
            flag.endswith("_Staged") or
            flag.endswith("_Rollout") or
            flag.endswith("_DataCenterFilter") or
            flag.endswith("_PlaceFilter")
        )
    ] + [
        "FStringFlagRepoGitHashFastString",
        "DFStringFlagRepoGitHashDynamicString",
        "FStringFlipTimeStampFastString",
        "DFStringFlipTimeStampDynamicString"
    ]
    for key in filter:
        fastflags.pop(key, None)

    return fastflags