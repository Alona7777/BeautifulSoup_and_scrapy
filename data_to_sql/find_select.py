from models_sql import session, Author, Quote, Tag, QuoteTag



def quote_by_tag(tag: str) -> list[str | None]:
    result = session.query(
        Author.id,
        Author.fullname,
        Quote.quote
        ).select_from(QuoteTag).join(Quote).join(Tag).join(Author).filter(Tag.name==tag).group_by(Quote.quote).all()
    res= []
    for item in result:
        line_res = f'AUTHOR ID and FULLNAME: {item[0]}. {item[1]}, QUOTE: {item[2]}'
        res.append(line_res)
    if len(res) == 0:
        return None
    else:
        return res

def quote_by_tag_id(tag_id: int ) -> list[str | None]:
    result = session.query(
        Author.id,
        Author.fullname,
        Quote.quote
        ).select_from(QuoteTag).join(Quote).join(Tag).join(Author).filter(Tag.id==tag_id).group_by(Quote.quote).all()
    res= []
    for item in result:
        line_res = f'AUTHOR ID and FULLNAME: {item[0]}. {item[1]}, QUOTE: {item[2]}'
        res.append(line_res)
    if len(res) == 0:
        return None
    else:
        return res
        
def quote_by_author_id(author: int) -> list[str | None]:
    result = session.query(
        Author.fullname,
        Quote.quote
        ).select_from(QuoteTag).join(Quote).join(Tag).join(Author).filter(Author.id==author).group_by(Quote.quote).all()
    res= []
    author_fullname = session.query(Author.fullname).filter(Author.id==author).first()[0]
    print(author_fullname)
    first_line = f'AUTHOR ID and FULLNAME: {author}. {author_fullname}'
    res.append(first_line)
    for item in result:
        line_res = f'QUOTE: {item[1]}'
        res.append(line_res)
    if len(res) == 0:
        return None
    else:
        return res

def author_by_quote_id(quote: int) -> list[str | None]:
    result = session.query(
        Quote.quote,
        Author.id,
        Author.fullname,
        Author.born_date,
        Author.description
        ).select_from(Quote).join(Author).filter(Quote.id==quote).group_by(Author.id).all()
    res= []
    for item in result:
        line_res = f'QUOTE: {item[0]}; AUTHOR ID: {item[1]}; AUTHOR FULLNAME: {item[2]}; AUTHOR BORN DATE: {item[3]}; AUTHOR DESCRIPTION: {item[4]}'
        res.append(line_res)
    if len(res) == 0:
        return None
    else:
        return res


if __name__ == '__main__':
    print(quote_by_tag('aa'))
    print(quote_by_tag_id(3))
    print(quote_by_author_id(2))
    print(author_by_quote_id(2))