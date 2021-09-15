package com.pinterest.deployservice.common;

import com.pinterest.deployservice.knox.CommandLineKnox;
import com.pinterest.deployservice.knox.FileSystemKnox;
import com.pinterest.deployservice.knox.Knox;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;


public class KnoxKeyManager {
    private final Logger LOG = LoggerFactory.getLogger(KnoxKeyManager.class);

    private Knox mKnox;

    private void registerKey(String key) throws Exception {
        File file = new File("/var/lib/knox/v0/keys/" + key);
        if (!file.exists()) {
            CommandLineKnox cmdKnox = new CommandLineKnox(key, Runtime.getRuntime());

            if (cmdKnox.register() != 0) {
                throw new RuntimeException("Error registering keys: " + key);
            }

            long startTime = System.currentTimeMillis();
            while (!file.exists() && System.currentTimeMillis() - startTime < 5000) {
                try {
                    Thread.sleep(100);
                }
                catch (InterruptedException ignore) {
                }
            }
        }
        mKnox = new FileSystemKnox(key);
    }

    public void init(String key) {
        try {
            LOG.info("Init the knox key with value {}", key);
            registerKey(key);
        } catch (Exception e) {
            LOG.error("Unable to register key due to exception :" + e.getMessage());
        }
    }

    public String getKey() {
        if (mKnox == null) {
            LOG.error("Returning null key since mKnox is null");
            return null;
        }
        try {
            String knoxKey = new String(mKnox.getPrimaryKey(), "UTF-8");
            return knoxKey;
        } catch (Exception e) {
            LOG.error("Returning null key due to exception :" + e.getMessage());
            return null;
        }
    }
}