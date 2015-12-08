import pytest
import attack.arpspoof


@pytest.fixture
def scapy_ether_obj(mocker):
    scapy_ether_mock = mocker.patch('attack.arpspoof.Ether').return_value
    return scapy_ether_mock


@pytest.fixture
def scapy_arp_obj(mocker):
    scapy_arp_mock = mocker.patch('attack.arpspoof.ARP').return_value
    return scapy_arp_mock


@pytest.fixture
def scapy_sendp_obj(mocker):
    scapy_sendp_mock = mocker.patch('attack.arpspoof.sendp').return_value
    return scapy_sendp_mock


@pytest.fixture
def multiprocessing_process_obj(mocker):
    multiprocessing_process_mock = mocker.patch('attack.arpspoof.Process').return_value
    return multiprocessing_process_mock


def test_mitm(mocker, scapy_ether_obj, scapy_arp_obj, scapy_sendp_obj, multiprocessing_process_obj):
    mock_open = mocker.patch('__builtin__.open', create=False).return_value.__enter__.return_value
    mock_open.readlines.return_value = True

    mitm = attack.arpspoof.MITM(
        {"mac": "6c:71:d9:2b:f3:59", "ip": "192.168.0.14"},
        {"mac": "f4:ca:e5:42:f6:c3", "ip": "192.168.0.254"}
    )
    mitm.start_spoof()
    mitm.spoof_someone({})


def test_mitm_valueerror(mocker, scapy_ether_obj, scapy_arp_obj, scapy_sendp_obj, multiprocessing_process_obj):
    mock_open = mocker.patch('__builtin__.open', create=False).return_value.__enter__.return_value
    mock_open.readlines.return_value = True

    with pytest.raises(ValueError):
        attack.arpspoof.MITM(
            0,
            {"mac": "f4:ca:e5:42:f6:c3", "ip": "192.168.0.254"}
        )

    with pytest.raises(ValueError):
        attack.arpspoof.MITM(
            {"mac": False, "ip": "192.168.0.14"},
            {"mac": "f4:ca:e5:42:f6:c3", "ip": "192.168.0.254"}
        )

    with pytest.raises(ValueError):
        mitm = attack.arpspoof.MITM(
            {"mac": "6c:71:d9:2b:f3:59", "ip": "192.168.0.14"},
            {"mac": "f4:ca:e5:42:f6:c3", "ip": "192.168.0.254"}
        )
        mitm.set_ip_forwarding("")




