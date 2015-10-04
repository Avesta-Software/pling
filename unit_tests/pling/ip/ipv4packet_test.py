
from binascii import hexlify

from pytest import fixture, raises

from pling.ip.ipv4packet import Ipv4RawPacket, Ipv4Packet

class Ipv4RawPacketTest:
    @fixture
    def subject(self):
        return Ipv4RawPacket()

    def saturated_packet(self):
        """Returns a packet with a different value for each field"""
        p = Ipv4RawPacket()
        p.dscp = 1
        p.ecn = 2
        p.identification = 3
        p.flags = 4
        p.fragment_offset = 5
        p.time_to_live = 6
        p.protocol = 7
        p.header_checksum = 8
        p.source_ip = 9
        p.destination_ip = 10

        p.payload = bytes([3, 1, 4, 2, 5, 7, 3, 5, 2])

        return p

    def example_packet(self):
        """Returns the example packet from this Wikipedia entry:

        https://en.wikipedia.org/wiki/IPv4_header_checksum
        """
        packet_hex = [
            # Header
            "45", "00", "00", "73", "00", "00", "40", "00", "40", "11",
            "b8", "61", "c0", "a8", "00", "01", "c0", "a8", "00", "c7",

            # Payload
            "00", "35", "e9", "7c", "00", "5f", "27", "9f", "1e", "4b",
            "81", "80"
        ]

        packet_bytes = bytes(int(x, 16) for x in packet_hex)

        return Ipv4RawPacket.from_bytes(packet_bytes)

    def test_eq(self, subject):
        """Two identical Ipv4RawPacket objects should == each other"""
        p1, p2 = self.saturated_packet(), self.saturated_packet()

        assert p1 == p2

        p2.protocol = 0

        assert p1 != p2

        p2.protocol = p1.protocol
        p2.payload = bytes([5, 3, 1, 6, 7, 5, 9, 2, 6])

        assert p1 != p2

    def test_bytes_empty_packet_length(self, subject):
        """An empty packet should be 20 bytes long"""
        assert len(bytes(subject)) == 20

    def test_from_bytes_selftest(self, subject):
        """Test if it can parse its own output"""
        p = self.saturated_packet()

        p2 = Ipv4RawPacket.from_bytes(bytes(p))

        msg = "Packets are not equal:\n\np1:\n{}\np2:\n{}".format(
            p.diagram(with_lines=True, with_captions=True),
            p2.diagram(with_lines=True)
        )

        assert p2 == p, msg

    def test_header_checksum(self, subject):
        """Tests that the header checksum is calculated correctly

        This test uses an example from Wikipedia:

            https://en.wikipedia.org/wiki/IPv4_header_checksum
        """
        p = self.example_packet()

        expected_checksum = int("B861", 16)

        assert p.generate_header_checksum() == expected_checksum

        # Changing a single bit should change the checksum
        p.version = 6

        assert p.generate_header_checksum() != expected_checksum

    def test_verify_checksum(self, subject):
        """Tests that verifying the header checksum works"""
        p = self.example_packet()

        assert p.verify_checksum()

        # Changing a single bit should make the checksum verification fail
        p.version += 1

        assert not p.verify_checksum()

class Ipv4PacketTest:
    @fixture
    def subject(self):
        return Ipv4Packet()

    def test_set_version(self, subject):
        """Tests that version is read-only"""
        with raises(AttributeError):
            subject.version = 6

    def test_get_version(self, subject):
        """Tests that the version is read from the raw packet"""
        subject.raw.version = 7

        assert subject.version == 7

    def test_get_protocol(self, subject):
        """Tests that get_protocol returns the protocol as a string"""
        subject.raw.protocol = 6

        assert subject.protocol == "TCP"

    def test_get_unknown_protocol(self, subject):
        """Tests that get_protocol fails when the raw protocol is unknown"""
        subject.raw.protocol = 1337

        with raises(ValueError) as e:
            subject.protocol

        assert "Unrecognized protocol" in str(e.value)

    def test_get_flags(self, subject):
        """Tests getting the flags as a set of strings"""
        subject.raw.flags = 3
        assert subject.flags == {"DF", "MF"}

        subject.raw.flags = 2
        assert subject.flags == {"DF"}

        subject.raw.flags = 1
        assert subject.flags == {"MF"}

        subject.raw.flags = 0
        assert subject.flags == set()

    def test_get_invalid_flags(self, subject):
        """Tests getting flags when the raw flags are invalid"""
        subject.raw.flags = 4

        with raises(ValueError) as e:
            subject.flags

        assert "Invalid raw flags" in str(e.value)

    def test_set_flags(self, subject):
        """Tests setting flags"""
        subject.flags = set()
        assert subject.raw.flags == 0b000

        subject.flags = {"DF"}
        assert subject.raw.flags == 0b010

        subject.flags = {"MF"}
        assert subject.raw.flags == 0b001

        subject.flags = {"DF", "MF"}
        assert subject.raw.flags == 0b011

    def test_set_raw_flags(self, subject):
        """Tests setting raw flags"""
        subject.flags = 3
        assert subject.raw.flags == 3

        subject.flags = 0
        assert subject.raw.flags == 0

    def test_set_invalid_flags(self, subject):
        """Tests setting invalid flags"""
        with raises(ValueError) as e:
            subject.flags = {"DF", "MF", "CSOAICJSOAID"}

        assert "Invalid flags" in str(e.value)

        with raises(TypeError) as e:
            subject.flags = 3.14

        assert "Expected flags to be int or iterable" in str(e.value)

    def test_set_invalid_raw_flags(self, subject):
        """Tests setting invalid raw flags"""
        with raises(ValueError) as e:
            subject.flags = 1337

        assert "Invalid flags" in str(e.value)

    def test_set_protocol_name(self, subject):
        """Tests setting protocol by name"""
        subject.protocol = "UDP"

        assert subject.raw.protocol == 17

    def test_set_unknown_protocol_name(self, subject):
        """Tests setting an unknown protocol name"""
        with raises(ValueError) as e:
            subject.protocol = "BDQOIDJSQNXSP"

        assert "Unrecognized protocol name" in str(e.value)

    def test_set_protocol_number(self, subject):
        """Tests setting protocol number"""
        subject.protocol = 6

        assert subject.raw.protocol == 6

    def test_test_unknown_protocol_number(self, subject):
        """Tests setting an unknown protocol number"""
        with raises(ValueError) as e:
            subject.protocol = 1337

        assert "Unrecognized protocol number" in str(e.value)
