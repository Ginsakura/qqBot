import nonebot,requests,re,json
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from datetime import datetime



# bot = nonebot.get_bot()

# @bot.on_message('group')
# async def _(ctx):
# 	user_id = ctx['user_id']
	# group_id = ctx['group_id']
	# await bot.send_group_msg(group_id = group_id,message = '你好～')
	# await bot.send_private_msg(user_id=user_id, message='你好～')



@on_command('抖音',aliases=('抖音解析'))
async def douyin(session: CommandSession):
	data = await parse_data(session.state['share_url'])
	await session.send(data)

@douyin.args_parser
async def parse_args(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
            session.state['share_url'] = stripped_arg
    elif not stripped_arg:
        session.finish('没有检测到分享链接，请重新输入')


async def parse_data(share_url):
	try:
		share_url = share_url.strip()
		pat = '(https://v.douyin.com/.*?/)'
		url = re.compile(pat).findall(share_url)[0]  #正则匹配分享链接
		headers = {'user-agent': 'Android',}
		res = requests.get(url, headers=headers, allow_redirects=False)		
		item_ids = res.text.split('/')[5]
		api = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={item_ids}'
		js_data = json.loads(requests.get(api,headers = headers).text)
		data = {}
		author_nickname = js_data['item_list'][0]['author']['nickname']
		douyin_desc = js_data['item_list'][0]['desc']
		douyin_create_time = datetime.fromtimestamp(js_data['item_list'][0]['create_time'])
		play_addr = js_data['item_list'][0]['video']['play_addr']['url_list'][0].replace('playwm','play')
		v_length = int(js_data['item_list'][0]['video']['duration'])
		data['author_nickname'] = author_nickname
		data['douyin_desc'] = douyin_desc
		data['play_addr'] = play_addr
		data['v_length'] = str(format(float(v_length/1000),".2f") + "s")
		data['douyin_create_time'] = douyin_create_time
		s = "作者:" + data['author_nickname'] + '\n' + "描述:" + data['douyin_desc'] + '\n' + "地址:" + data['play_addr'] + '\n' + '时长:' + data['v_length'] + '\n' + '发布时间:' + str(data['douyin_create_time'])
		return str(s)
	except:
		return "哭辽~~o(>_<)o ~~，解析失败！"

