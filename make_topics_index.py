from lxml import html
import requests
import time


min_topic_id = 3      # first thread
max_topic_id = 87698  # "we're closing down the Sporum" thread
page_url_format = 'http://forum.spore.com/jforum/posts/list/{0}/{1}.page'

tsv_cols = ['id', 'op', 'page_count', 'category', 'title']


def page_url(topic_id, page):
    page_id = (page - 1) * 15
    return page_url_format.format(page_id, topic_id)


def topic_url(topic_id):
    return page_url(topic_id, 1)


def scrape_topic(topic_id):
    url = topic_url(topic_id)
    page = requests.get(url)
    tree = html.fromstring(page.content)

    # get title
    title_els = tree.cssselect('.maintitle')
    if not title_els:
        return None  # if no title element, this is a void topic. bail out!
    title = title_els[0].text_content()

    # get category
    nav_els = tree.cssselect('a.nav')
    if len(nav_els) < 2:
        return None  # if no category, this is a void topic. bail out!
    category = nav_els[1].text_content()

    # get usernames of posters on this page
    usernames = [el.text_content() for el in tree.cssselect('.genmed')]
    if not usernames:
        return None  # if no usernames, this is a void topic. bail out!
    op_username = usernames[0]

    # get page count
    page_numbers = [el.text_content() for el in tree.cssselect('.pagination a')]
    # The last two pagination buttons are a "next page" arrow and "Go" button,
    # so the actual last page number is third from the end.
    # If the topic only has one page, there's no pagination buttons at all.
    page_count = int(page_numbers[-3]) if page_numbers else 1

    return {
        'id': topic_id,
        'title': title,
        'category': category,
        'op': op_username,
        'page_count': page_count
    }


def main():
    # some sample topics – #3 is a one-pager, #300 is a many-pager
    #print(scrape_topic(3))
    #print(scrape_topic(300))

    tsv_headers = '\t'.join(tsv_cols)
    print(tsv_headers)
    with open('./topics.tsv', 'w+') as tsv:
        tsv.write(tsv_headers + '\n')
        for topic_id in range(min_topic_id, max_topic_id + 1):
            topic = scrape_topic(topic_id)
            if not topic:
                print(str(topic_id) + ': no data')
                continue
            tsv_line = '\t'.join([str(topic[col]) for col in tsv_cols])
            print(tsv_line)
            tsv.write(tsv_line + '\n')
            time.sleep(1)  # to avoid overwhelming the poor server :(

main()
