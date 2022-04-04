# Avlos

Given a tree that represents a remote embedded device, Avlos will generate code (embedded, client) for the remote client to talk to the device. 

## Example

Given a device description expressed in a YAML file as follows:

    name: toaster
    attributes:
    - name: sn
        dtype: uint32
        c_getter: toaster_get_sn
        description: The unique device serial number.
    - name: heater
      attributes:
      - name: temperature
          dtype: float
          unit: celsius
          c_getter: toaster_get_heater_temp
          description: The toaster heater temperature.
    - name: relay
      attributes:
      - name: relay_state
          dtype: bool
          c_getter: toaster_get_relay_state
          c_setter: toaster_set_relay_state
          description: The toaster heating relay element state.


, by default Avlos will generate the following C header(note: there are actually a few more stuff not included here for brevity):

    /*
    * avlos_toaster_sn
    *
    * The unique device serial number.
    *
    * @param buffer
    * @param buffer_len
    * @param rtr
    */
    uint8_t avlos_toaster_sn(uint8_t * buffer, uint8_t * buffer_len, bool rtr);

    /*
    * avlos_toaster_heater_temp
    *
    * The toaster heater temperature.
    *
    * @param buffer
    * @param buffer_len
    * @param rtr
    */
    uint8_t avlos_toaster_heater_temp(uint8_t * buffer, uint8_t * buffer_len, bool rtr);

    /*
    * avlos_toaster_relay_state
    *
    * The toaster heating relay element state.
    *
    * @param buffer
    * @param buffer_len
    * @param rtr
    */
    uint8_t avlos_toaster_relay_state(uint8_t * buffer, uint8_t * buffer_len, bool rtr);


, implementation:

    uint8_t avlos_toaster_sn(uint8_t * buffer, uint8_t * buffer_len, bool rtr)
    {
        uint32_t v;
        if (AVLOS_DIR_READ == buffer[0]) {
            v = toaster_get_sn();
            *buffer_len = sizeof(v);
            memcpy(buffer+1, &v, sizeof(v));
            return AVLOS_RET_READ;
        }
    return AVLOS_RET_NOACTION;
    }

    uint8_t avlos_toaster_heater_temp(uint8_t * buffer, uint8_t * buffer_len, bool rtr)
    {
        uint32_t v;
        if (AVLOS_DIR_READ == buffer[0]) {
            v = toaster_get_heater_temp();
            *buffer_len = sizeof(v);
            memcpy(buffer+1, &v, sizeof(v));
            return AVLOS_RET_READ;
        }
    return AVLOS_RET_NOACTION;
    }

    uint8_t avlos_toaster_relay_state(uint8_t * buffer, uint8_t * buffer_len, bool rtr)
    {
        float v;
        if (AVLOS_DIR_READ == buffer[0]) {
            v = toaster_get_relay_state();
            *buffer_len = sizeof(v);
            memcpy(buffer+1, &v, sizeof(v));
            return AVLOS_RET_READ;
        }
        else if (AVLOS_DIR_WRITE == buffer[0]) {
            memcpy(&v, buffer+1, sizeof(v));
            toaster_set_relay_state(v);
            return AVLOS_RET_WRITE;
        }
        return AVLOS_RET_NOACTION;
    }


, and the following RestructuredText documentation:

    toaster.sn
    ----------

    - Endpoint ID: 1
    - Data Type: uint32
    - Unit: Not defined

    The unique device serial number.

    toaster.heater.temperature
    --------------------------

    - Endpoint ID: 2
    - Data Type: float
    - Unit: degree_Celsius

    The toaster heater temperature.

    toaster.relay.state
    --------------------------

    - Endpoint ID: 3
    - Data Type: bool
    - Unit: Not defined

    The toaster heating element relay state.


It will also compute a checksum for the spec and add it as a getter function so that it can be retrieved by the client for comparing client and device specs. 

The output location, as well as many other attributes of the files are configurable.