import asyncio

async def sec_f(n):
    while True:
        print('I am second function{}'.format(n))
        await asyncio.sleep(n)



async def start():
    print ('I am first1')
    mytask1 = asyncio.create_task (sec_f(4))
    mytask2 = asyncio.create_task (sec_f (1))
    await mytask1
    await mytask2
    print('I am first2')




asyncio.run(start())
print('go to next')
asyncio.run(start())
