from mongoengine import *

connect("tumbledb")


# =============================================

# john = User(email='john@example.com', first_name='john', last_name='Lawley')
# john.save()
# ross = User(email='ross@example.com', first_name='Ross', last_name='Lawley')
# ross.save()

# post1 = TextPost(title='Fun with MongoEngine$', author=john)
# post1.content = 'Took a look at MongoEngine today, looks pretty cool.'
# post1.tags = ['mongodb', 'mongoengine']
# post1.save()

# post2 = LinkPost(title='MongoEngine Documentation$', author=ross)
# post2.link_url = 'http://docs.mongoengine.com/'
# post2.tags = ['mongoengine']
# post2.save()

# for post in Post.objects:
#     print(post.title)
# print()
# for post in TextPost.objects:
#     print(post.title)

# for post in Post.objects:
#     print(f'{post.title} \nAuthor --> {post.author.first_name} {post.author.last_name}' )
#     print('=' * len(post.title))

#     if isinstance(post, TextPost):
#         print( post.content)
#         print()

#     if isinstance(post, LinkPost):
#         print( 'Link:', post.link_url)
#         print()

#     print
