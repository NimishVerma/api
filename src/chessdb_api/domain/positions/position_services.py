from chessdb_api.domain import base_schemas
from chessdb_api.domain.positions import position_queries
from chessdb_api.domain.positions import position_schemas
import pydantic


class Service:
    """Service.
    """

    def __init__(self, queries: position_queries.Queries):
        self._queries = queries

    async def create(self,
                     position: position_schemas.Create) -> position_schemas.DB:
        position_with_bitboards = position_schemas.DB(fen=position.fen,
                                                      bitboard_all=1,
                                                      bitboard_white=1,
                                                      bitboard_black=1,
                                                      bitboard_white_pawn=1,
                                                      bitboard_black_pawn=1,
                                                      bitboard_white_rook=1,
                                                      bitboard_black_rook=1,
                                                      bitboard_white_knight=1,
                                                      bitboard_black_knight=1,
                                                      bitboard_white_bishop=1,
                                                      bitboard_black_bishop=1,
                                                      bitboard_white_queen=1,
                                                      bitboard_black_queen=1,
                                                      bitboard_white_king=1,
                                                      bitboard_black_king=1)
        new_position = await self._queries.create(
            position=position_with_bitboards)
        return position_schemas.DB.from_orm(new_position)

    async def get_by_id(self, fen: str) -> position_schemas.DB:
        position = await self._queries.get_by_id(fen=fen)
        if position:
            return position_schemas.DB.from_orm(position)
        return None

    async def get_list(
        self,
        page: pydantic.conint(ge=1),
        page_size: pydantic.conint(ge=1, le=100),
    ) -> position_schemas.Paginated:
        positions, total = await self._queries.get_list(page=page,
                                                        page_size=page_size)
        more = ((total / page_size) - page) > 0
        results = [
            position_schemas.DB.from_orm(position) for position in positions
        ]
        pagination = base_schemas.Pagination(total=total, more=more)
        return position_schemas.Paginated(results=results,
                                          pagination=pagination)

    async def update(
            self, fen: str,
            new_position: position_schemas.Update) -> position_schemas.DB:
        old_position = await self._queries.get_by_id(fen=fen)
        updated_position = await self._queries.update(old_position=old_position,
                                                      new_position=new_position)
        return position_schemas.DB.from_orm(updated_position)

    async def delete(self, fen: str) -> position_schemas.DB:
        deleted_position = await self._queries.delete(fen=fen)
        return position_schemas.DB.from_orm(deleted_position)
