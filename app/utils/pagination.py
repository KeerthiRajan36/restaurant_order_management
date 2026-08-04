from math import ceil


def paginate(
    query,
    page: int = 1,
    limit: int = 10
):

    total = query.count()

    pages = ceil(total / limit) if total else 1

    results = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "page": page,
        "limit": limit,
        "total_records": total,
        "total_pages": pages,
        "data": results
    }