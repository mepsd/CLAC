import { serializers, deserializers } from '../serialization';
import { DEFAULT_SORT, MAX_QUERY_LENGTH } from '../constants';

describe('sort deserializer', () => {
  const { sort } = deserializers;

  it('returns default sort when invalid', () => {
    expect(sort('')).toEqual(DEFAULT_SORT);
    expect(sort('-')).toEqual(DEFAULT_SORT);
    expect(sort('LOL')).toEqual(DEFAULT_SORT);
    expect(sort('-LOL')).toEqual(DEFAULT_SORT);
  });

  it('returns descending sort when preceded by "-"', () => {
    expect(sort('-labor_category')).toEqual({
      key: 'labor_category',
      descending: true,
    });
  });

  it('returns ascending sort when not preceded by "-"', () => {
    expect(sort('vendor_name')).toEqual({
      key: 'vendor_name',
      descending: false,
    });
  });
});

describe('sort serializer', () => {
  const { sort } = serializers;

  it('prepends "-" if descending', () => {
    expect(sort({ descending: true, key: 'blah' })).toBe('-blah');
  });
  it('does not prepend "-" if ascending', () => {
    expect(sort({ descending: false, key: 'blah' })).toBe('blah');
  });
});

describe('q deserializer', () => {
  const { q } = deserializers;

  it('truncates to MAX_QUERY_LENGTH', () => {
    const query = Array(MAX_QUERY_LENGTH + 10).join('x');
    expect(q(query).length).toBe(MAX_QUERY_LENGTH);
  });
});

describe('q serializer', () => {
  const { q } = serializers;

  it('truncates to MAX_QUERY_LENGTH', () => {
    const query = Array(MAX_QUERY_LENGTH + 10).join('x');
    expect(q(query).length).toBe(MAX_QUERY_LENGTH);
  });
});
