#  Copyright (c) 2021. https://m2aglabs.com
#
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from device.things.valuehelper import ValueHelper as Value
from webthing import (Property)


class ThingBuilder:

    @staticmethod
    def add_props(config, thing):
        """
            Each property will have a class member for it's value object. This will
            simplify the types of value object to create.
        """

        for p in config['thing']['props']:
            _set = 'None'
            _opts = {}
            pr = config['thing']['props'][p]

            _get = pr['value'][0]
            _set = pr['value'][1]
            if len(pr['value']) == 3:
                _opts = pr['value'][2]

            if isinstance(_get, str):
                _get = thing.component.get(_get)

            # TODO: add index back to this
            if _set != 'None':   # This is comparing a string
                vl = Value(_get, lambda v: thing.component.set(v), _opts)
            else:
                vl = Value(_get, None, _opts)

            setattr(thing, pr['name'], vl)
            prop = Property(thing, pr['name'], getattr(thing, pr['name']), pr['metadata'])
            thing.add_property(prop)

    @staticmethod
    def add_events(config, thing):
        pass

    @staticmethod
    def add_action(config, thing):
        pass
