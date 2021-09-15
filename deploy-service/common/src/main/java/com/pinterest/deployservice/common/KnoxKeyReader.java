package com.pinterest.deployservice.common;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class KnoxKeyReader {

    private static final Logger LOG = LoggerFactory.getLogger(KnoxKeyReader.class);

    private String testKey = "key";

    private KnoxKeyManager knoxManager;

    public void init(String key) {
        if (knoxManager == null) {
            knoxManager = new KnoxKeyManager();
            knoxManager.init(key);
        }
    }

    public String getKey() {
        if (knoxManager == null) {
            LOG.error("Using default key since knoxManager is null");
            return testKey;
        }
        try {
            String knoxKey = knoxManager.getKey();
            return knoxKey;
        } catch (Exception e) {
            LOG.error("Using default key due to exception :" + e.getMessage());
            return testKey;
        }
    }
}