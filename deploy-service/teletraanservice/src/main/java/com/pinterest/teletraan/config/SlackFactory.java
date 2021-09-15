/**
 * Copyright 2016 Pinterest, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *  
 *     http://www.apache.org/licenses/LICENSE-2.0
 *    
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.pinterest.teletraan.config;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonTypeName;
import com.pinterest.deployservice.chat.ChatManager;
import com.pinterest.deployservice.chat.SlackChatManager;
import org.hibernate.validator.constraints.NotEmpty;

@JsonTypeName("slack")
public class SlackFactory implements ChatFactory {
    @NotEmpty
    @JsonProperty
    private String knoxKey;

    public String getKnoxKey() {
        return knoxKey;
    }

    public void setKnoxKey(String knoxKey) {
        this.knoxKey = knoxKey;
    }

    @Override
    public ChatManager create() throws Exception {
        return new SlackChatManager(knoxKey);
    }
}
