#!/usr/bin/env python3

import time
from prometheus_client import start_http_server, Gauge
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
import configparser
import argparse
from unifi import unifi
import pprint

PORT = 9108

class UnifiCollector(object):
    def __init__(self, configfile):
        self.readconfig(configfile)
        self.unifi = unifi.UniFi(self.apiendpoint, self.apiusername, self.apipassword)

    def readconfig(self, configfile):
        config = configparser.ConfigParser()
        config.read(configfile)
        self.apiendpoint = config.get('API','URL')
        self.apiusername = config.get('API','Username')
        self.apipassword = config.get('API','Password')

        # Just as a help really, code will not be reached as config.get() will blow up
        if self.apiendpoint is None:
            raise AssertionError('API/URL is required in configuration')
        if self.apiusername is None or self.apipassword is None:
            raise AssertionError('API/Username and API/Password is required in configuration')

    def collect(self):
        c_sta_rx_bytes = CounterMetricFamily('unifi_sta_rx_bytes', 'Client RX bytes',    labels=['mac', 'hostname', 'radio', 'essid'])
        c_sta_tx_bytes = CounterMetricFamily('unifi_sta_tx_bytes', 'Client TX bytes',    labels=['mac', 'hostname', 'radio', 'essid'])
        g_sta_rssi     = GaugeMetricFamily('unifi_sta_rssi',       'Client signal RSSI', labels=['mac', 'hostname', 'radio', 'essid'])

        c_port_rx_bytes   = CounterMetricFamily('unifi_port_rx_bytes',   'Port RX bytes',   labels=['port', 'mac', 'name', 'model'])
        c_port_tx_bytes   = CounterMetricFamily('unifi_port_tx_bytes',   'Port TX bytes',   labels=['port', 'mac', 'name', 'model'])
        c_port_rx_errors  = CounterMetricFamily('unifi_port_rx_errors',  'Port RX errors',  labels=['port', 'mac', 'name', 'model'])
        c_port_tx_errors  = CounterMetricFamily('unifi_port_tx_errors',  'Port TX errors',  labels=['port', 'mac', 'name', 'model'])
        c_port_rx_packets = CounterMetricFamily('unifi_port_rx_packets', 'Port RX packets', labels=['port', 'mac', 'name', 'model'])
        c_port_tx_packets = CounterMetricFamily('unifi_port_tx_packets', 'Port TX packets', labels=['port', 'mac', 'name', 'model'])
        c_port_rx_dropped = CounterMetricFamily('unifi_port_rx_dropped', 'Port RX dropped', labels=['port', 'mac', 'name', 'model'])
        c_port_tx_dropped = CounterMetricFamily('unifi_port_tx_dropped', 'Port TX dropped', labels=['port', 'mac', 'name', 'model'])

        g_port_poe_current = GaugeMetricFamily('unifi_port_poe_current', 'Port POE current', labels=['port', 'mac', 'name', 'model'])
        g_port_poe_power   = GaugeMetricFamily('unifi_port_poe_power',   'Port POE power',   labels=['port', 'mac', 'name', 'model'])
        g_port_poe_voltage = GaugeMetricFamily('unifi_port_poe_voltage', 'Port POE voltage', labels=['port', 'mac', 'name', 'model'])

        c_vap_rx_bytes   = CounterMetricFamily('unifi_vap_rx_bytes',   'VAP RX bytes',   labels=['radio', 'essid', 'mac', 'name', 'model'])
        c_vap_tx_bytes   = CounterMetricFamily('unifi_vap_tx_bytes',   'VAP TX bytes',   labels=['radio', 'essid', 'mac', 'name', 'model'])
        c_vap_rx_errors  = CounterMetricFamily('unifi_vap_rx_errors',  'VAP RX errors',  labels=['radio', 'essid', 'mac', 'name', 'model'])
        c_vap_tx_errors  = CounterMetricFamily('unifi_vap_tx_errors',  'VAP TX errors',  labels=['radio', 'essid', 'mac', 'name', 'model'])
        c_vap_rx_packets = CounterMetricFamily('unifi_vap_rx_packets', 'VAP RX packets', labels=['radio', 'essid', 'mac', 'name', 'model'])
        c_vap_tx_packets = CounterMetricFamily('unifi_vap_tx_packets', 'VAP TX packets', labels=['radio', 'essid', 'mac', 'name', 'model'])
        c_vap_rx_dropped = CounterMetricFamily('unifi_vap_rx_dropped', 'VAP RX dropped', labels=['radio', 'essid', 'mac', 'name', 'model'])
        c_vap_tx_dropped = CounterMetricFamily('unifi_vap_tx_dropped', 'VAP TX dropped', labels=['radio', 'essid', 'mac', 'name', 'model'])
        c_vap_num_sta    = GaugeMetricFamily('unifi_vap_num_sta', 'VAP Client count',    labels=['radio', 'essid', 'mac', 'name', 'model'])

        c_uplink_rx_bytes   = CounterMetricFamily('unifi_uplink_rx_bytes',   'Uplink RX bytes',   labels=['mac', 'name', 'model'])
        c_uplink_tx_bytes   = CounterMetricFamily('unifi_uplink_tx_bytes',   'Uplink TX bytes',   labels=['mac', 'name', 'model'])
        c_uplink_rx_errors  = CounterMetricFamily('unifi_uplink_rx_errors',  'Uplink RX errors',  labels=['mac', 'name', 'model'])
        c_uplink_tx_errors  = CounterMetricFamily('unifi_uplink_tx_errors',  'Uplink TX errors',  labels=['mac', 'name', 'model'])
        c_uplink_rx_packets = CounterMetricFamily('unifi_uplink_rx_packets', 'Uplink RX packets', labels=['mac', 'name', 'model'])
        c_uplink_tx_packets = CounterMetricFamily('unifi_uplink_tx_packets', 'Uplink TX packets', labels=['mac', 'name', 'model'])
        c_uplink_rx_dropped = CounterMetricFamily('unifi_uplink_rx_dropped', 'Uplink RX dropped', labels=['mac', 'name', 'model'])
        c_uplink_tx_dropped = CounterMetricFamily('unifi_uplink_tx_dropped', 'Uplink TX dropped', labels=['mac', 'name', 'model'])

        g_loadavg_1         = GaugeMetricFamily('unifi_loadavg_1',       'Loadavg 1',     labels=['mac', 'name', 'model'])
        g_loadavg_5         = GaugeMetricFamily('unifi_loadavg_5',       'Loadavg 5',     labels=['mac', 'name', 'model'])
        g_loadavg_15        = GaugeMetricFamily('unifi_loadavg_15',      'Loadavg 15',    labels=['mac', 'name', 'model'])
        g_mem_total         = GaugeMetricFamily('unifi_mem_total',       'Memory total',  labels=['mac', 'name', 'model'])
        g_mem_used          = GaugeMetricFamily('unifi_mem_used',        'Memory used',   labels=['mac', 'name', 'model'])
        g_mem_buffer        = GaugeMetricFamily('unifi_mem_buffer',      'Memory buffers',labels=['mac', 'name', 'model'])
        g_general_temperature= GaugeMetricFamily('unifi_general_temperature',      'General temperature',labels=['mac', 'hostname'])

        for site in self.unifi.sites():
            self.unifi.debug('SITE: ' + site.name)
            for dev in site.device():
                if dev.model == 'U7PG2' or dev.model == 'U7HD':
                    for vap in dev.vap:
                        if vap.get('t') is None or vap['t'] != 'vap':
                            continue

                        labels = [
                                self.radio_str(vap.get('radio')),
                                vap.get('essid'),
                                dev.mac,
                                dev.name,
                                dev.model
                                ]
                        if vap.get('rx_bytes') is not None:
                            c_vap_rx_bytes.add_metric(labels,   int(vap.get('rx_bytes')))
                            c_vap_rx_errors.add_metric(labels,  int(vap.get('rx_errors')))
                            c_vap_rx_packets.add_metric(labels, int(vap.get('rx_packets')))
                            c_vap_rx_dropped.add_metric(labels, int(vap.get('rx_dropped')))

                        if vap.get('tx_bytes') is not None:
                            c_vap_tx_bytes.add_metric(labels,   int(vap.get('tx_bytes')))
                            c_vap_tx_errors.add_metric(labels,  int(vap.get('tx_errors')))
                            c_vap_tx_packets.add_metric(labels, int(vap.get('tx_packets')))
                            c_vap_tx_dropped.add_metric(labels, int(vap.get('tx_dropped')))

                        if vap.get('num_sta') is not None:
                            c_vap_num_sta.add_metric(labels,    int(vap.get('num_sta')))

                elif dev.model == 'US8P150':
                    for idx, port in dev.port.items():
                        labels = [
                                str(port.get('port_idx')),
                                dev.mac,
                                dev.name,
                                dev.model
                                ]

                        if port.get('rx_bytes') is not None:
                            c_port_rx_bytes.add_metric(labels,   int(port.get('rx_bytes')))
                            c_port_rx_errors.add_metric(labels,  int(port.get('rx_errors')))
                            c_port_rx_packets.add_metric(labels, int(port.get('rx_packets')))
                            c_port_rx_dropped.add_metric(labels, int(port.get('rx_dropped')))

                        if port.get('tx_bytes') is not None:
                            c_port_tx_bytes.add_metric(labels,   int(port.get('tx_bytes')))
                            c_port_tx_errors.add_metric(labels,  int(port.get('tx_errors')))
                            c_port_tx_packets.add_metric(labels, int(port.get('tx_packets')))
                            c_port_tx_dropped.add_metric(labels, int(port.get('tx_dropped')))

                        if port.get('poe_current') is not None:
                            g_port_poe_current.add_metric(labels, float(port.get('poe_current')))
                            g_port_poe_power.add_metric(labels,   float(port.get('poe_power')))
                            g_port_poe_voltage.add_metric(labels, float(port.get('poe_voltage')))

                    labels = [
                            dev.mac,
                            dev.name,
                            dev.model
                            ]
                    if dev.general_temperature is not None:
                        g_general_temperature.add_metric(labels, float(dev.general_temperature))
                elif dev.model == 'UGW3':
                    for idx, port in dev.ports.items():
                        labels = [
                                port.get('name'),
                                dev.mac,
                                dev.name,
                                dev.model
                                ]

                        if port.get('rx_bytes') is not None:
                            c_port_rx_bytes.add_metric(labels,   int(port.get('rx_bytes')))
                            c_port_rx_errors.add_metric(labels,  int(port.get('rx_errors')))
                            c_port_rx_packets.add_metric(labels, int(port.get('rx_packets')))
                            c_port_rx_dropped.add_metric(labels, int(port.get('rx_dropped')))

                        if port.get('tx_bytes') is not None:
                            c_port_tx_bytes.add_metric(labels,   int(port.get('tx_bytes')))
                            c_port_tx_errors.add_metric(labels,  int(port.get('tx_errors')))
                            c_port_tx_packets.add_metric(labels, int(port.get('tx_packets')))
                            c_port_tx_dropped.add_metric(labels, int(port.get('tx_dropped')))
                else:
                    self.unifi.debug('Cannot collect stats for device of model ' + dev.model)
                    continue

                labels = [
                        dev.mac,
                        dev.name,
                        dev.model
                        ]
                if dev.uplink:
                    c_uplink_rx_bytes.add_metric(labels,   int(dev.uplink.get('rx_bytes')))
                    c_uplink_tx_bytes.add_metric(labels,   int(dev.uplink.get('tx_bytes')))
                    c_uplink_rx_errors.add_metric(labels,  int(dev.uplink.get('rx_errors')))
                    c_uplink_tx_errors.add_metric(labels,  int(dev.uplink.get('tx_errors')))
                    c_uplink_rx_packets.add_metric(labels, int(dev.uplink.get('rx_packets')))
                    c_uplink_tx_packets.add_metric(labels, int(dev.uplink.get('tx_packets')))
                    c_uplink_rx_dropped.add_metric(labels, int(dev.uplink.get('rx_dropped')))
                    c_uplink_tx_dropped.add_metric(labels, int(dev.uplink.get('tx_dropped')))
                if dev.sysstat:
                    g_loadavg_1.add_metric(labels, float(dev.sysstat.get('loadavg_1')))
                    g_loadavg_5.add_metric(labels, float(dev.sysstat.get('loadavg_5')))
                    g_loadavg_15.add_metric(labels, float(dev.sysstat.get('loadavg_15')))
                    g_mem_total.add_metric(labels, float(dev.sysstat.get('mem_total')))
                    g_mem_used.add_metric(labels, float(dev.sysstat.get('mem_used')))
                    g_mem_buffer.add_metric(labels, float(dev.sysstat.get('mem_buffer')))

            for client in site.sta():
                if client.get('rx_bytes') is None:
                    continue

                labels = [
                            client.get('mac'),
                            client.get('hostname') or client.get('mac'),
                            self.radio_str(client.get('radio')) or '',
                            client.get('essid') or ''
                        ]

                c_sta_rx_bytes.add_metric(labels, int(client.get('rx_bytes')))
                c_sta_tx_bytes.add_metric(labels, int(client.get('tx_bytes')))
                if client.get('rssi') is not None:
                    g_sta_rssi.add_metric(labels, int(client.get('rssi')))

        yield c_sta_rx_bytes
        yield c_sta_tx_bytes
        yield g_sta_rssi

        yield c_port_rx_bytes
        yield c_port_tx_bytes
        yield c_port_rx_errors
        yield c_port_tx_errors
        yield c_port_rx_packets
        yield c_port_tx_packets
        yield c_port_rx_dropped
        yield c_port_tx_dropped

        yield g_port_poe_current
        yield g_port_poe_power
        yield g_port_poe_voltage

        yield c_vap_rx_bytes
        yield c_vap_tx_bytes
        yield c_vap_rx_errors
        yield c_vap_tx_errors
        yield c_vap_rx_packets
        yield c_vap_tx_packets
        yield c_vap_rx_dropped
        yield c_vap_tx_dropped
        yield c_vap_num_sta

        yield c_uplink_rx_bytes
        yield c_uplink_tx_bytes
        yield c_uplink_rx_errors
        yield c_uplink_tx_errors
        yield c_uplink_rx_packets
        yield c_uplink_tx_packets
        yield c_uplink_rx_dropped
        yield c_uplink_tx_dropped

        yield g_loadavg_1
        yield g_loadavg_5
        yield g_loadavg_15
        yield g_mem_total
        yield g_mem_used
        yield g_mem_buffer
        yield g_general_temperature

    def radio_str(self, s):
        if s is None:
            return None
        elif s == 'na':
            return '5'
        elif s == 'ng':
            return '2.4'
        else:
            return s

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='UniFi Prometheus exporter')
    parser.add_argument('--port', dest='port', default=PORT, help='Port to listen to')
    parser.add_argument('--config', dest='config', default=None, required=True, help='Configuration file for API')

    args = parser.parse_args()
    configfile = args.config
    port = args.port

    REGISTRY.register(UnifiCollector(configfile))
    start_http_server(port)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Break")

exit(0)
