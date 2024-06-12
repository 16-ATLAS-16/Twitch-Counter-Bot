import asyncio
import constructor, asyncTK
from asyncTK import AsyncTK

test = AsyncTK(title='test program', size=(200, 100))
const = constructor.TKConstructor(test.root)
a = const.construct([{'construct': 
                            {'widget': 'Button'},
                  'settings': 
                            {'text': 'hello world!', 'fg': 'red'}},
                 {'construct': 
                            {'widget': 'frame'},
                  'settings': 
                            {'bg':'blue'},
                  'children':
                            [
                                {
                                    'construct': {
                                        'widget': 'label'
                                    },
                                    'settings': {
                                        'text': 'hello world! from widget!'
                                    }
                                },
                                {
                                    'construct': {
                                        'widget': 'frame'
                                    },
                                    'settings': {
                                        'bg': 'blue'
                                    },
                                    'children': 
                                        [
                                            {
                                                'construct': {
                                                    'widget': 'label'
                                                },
                                                'settings': {
                                                    'text': 'hello world from sub-child!',
                                                    'fg': 'purple'
                                                }
                                            }
                                        ]
                                    
                                }
                            ]}
                  ])
print(a)
asyncio.run(test.render())